const cartGrid = document.querySelector('.cart__grid');
const totalQuantityInCartIcon = document.querySelector(
  '.header__cart-button p'
);
const incrementButtons = document.querySelectorAll('[id^="increment"]');
const decrementButtons = document.querySelectorAll('[id^="decrement"]');

const cart_total = document.getElementById('cart-total');
const tax = document.getElementById('tax');
const delivery = document.getElementById('delivery');
const sub_total = document.getElementById('sub-total');

/* Fetch Post */
async function fetchPost(url) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
  });

  const data = await response.json();

  return data;
}

/* Update checkout and total quantity */
function updatedCheckout(checkout) {
  // update checkout section
  cart_total.innerHTML = checkout['cart_total'];
  tax.innerHTML = checkout['tax'];
  delivery.innerHTML = checkout['delivery'];
  sub_total.innerHTML = checkout['sub_total'];
  // update total quantity in header cart icon
  totalQuantityInCartIcon.innerHTML = checkout['total_quantity'];
}

/* Update product quantity and total price each product in each cart item */
function updateCartItem(productId, orient) {
  // update quantity value
  const quantity = document.querySelector(`#product-quantity-${productId}`);
  const previousQuantity = Number(quantity.innerHTML);

  if (orient === 'inc') {
    quantity.innerHTML = previousQuantity + 1;
  } else {
    quantity.innerHTML = previousQuantity - 1;
  }

  // update total_price of each product
  const price = document.querySelector(`#price-${productId}`);
  const total_price = document.querySelector(`#total-price-${productId}`);
  let updatedTotalPrice = Number(price.innerHTML) * Number(quantity.innerHTML);
  total_price.innerHTML = updatedTotalPrice;

  if (orient === 'dec') {
    if (previousQuantity === 1) {
      // Remove cart item from cart detail page
      const cartItem = document.querySelector(`#cart-item-${productId}`);
      cartGrid.removeChild(cartItem);
    }
  }
}

// Increment the quantity of an item by 1
incrementButtons.forEach((inc) => {
  inc.addEventListener('click', () => {
    const productId = inc.id.split('-')[1];

    fetchPost(`/cart/add/${productId}/`).then((data) => {
      if (data['status'] === 'ok') {
        updateCartItem(productId, 'inc');
        updatedCheckout(data['checkout']);
      }
    });
  });
});

// Decrement the quantity of an item by 1
decrementButtons.forEach((dec) => {
  dec.addEventListener('click', () => {
    const productId = dec.id.split('-')[1];

    fetchPost(`/cart/remove/${productId}/`).then((data) => {
      if (data['status'] === 'ok') {
        updateCartItem(productId, 'dec');
        updatedCheckout(data['checkout']);
      }
    });
  });
});

// Clear item from the cart
clearItemButtons = document.querySelectorAll('.cart__close');

clearItemButtons.forEach((clearBtn) => {
  clearBtn.addEventListener('click', () => {
    const productId = clearBtn.id.split('-')[2];

    fetchPost(`/cart/clear/${productId}/`).then((data) => {
      if (data['status'] === 'ok') {
        updatedCheckout(data['checkout']);

        // Remove cart item from cart detail page
        const cartItem = document.querySelector(`#cart-item-${productId}`);
        cartGrid.removeChild(cartItem);
      }
    });
  });
});
