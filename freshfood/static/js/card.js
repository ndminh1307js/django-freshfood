const orderButtons = document.querySelectorAll('.card__button--order');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const totalQuantityInCartIcon = document.querySelector(
  '.header__cart-button p'
);

const languageCode = document.querySelector('#current-language').value;

orderButtons.forEach((orderBtn) => {
  orderBtn.addEventListener('click', (e) => {
    e.preventDefault();

    const productId = orderBtn.id.split('-')[1];

    fetch(`/${languageCode}/cart/add/${productId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data['status'] == 'ok') {
          // update total quantity in header cart icon
          totalQuantityInCartIcon.innerHTML =
            data['checkout']['total_quantity'];
        }
      });
  });
});
