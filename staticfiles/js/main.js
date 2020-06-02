const menuButton = document.querySelector(".header__menu-button");
const navigation = document.querySelector(".navigation");
const body = document.querySelector("body");

function lockScrollBody() {
  // Lock scroll document when navigation visible
  if (body.classList.contains("lock-scroll")) {
    body.classList.remove("lock-scroll");
  } else {
    body.classList.add("lock-scroll");
  }
}

// Click hamburger to toggle navigation
menuButton.addEventListener("click", () => {
  if (menuButton.classList.contains("visible")) {
    menuButton.classList.remove("visible");
    navigation.style.display = "none";
  } else {
    menuButton.classList.add("visible");
    navigation.style.display = "block";
  }

  lockScrollBody();
});

// Click outside navigation list to close navigation
window.addEventListener("click", (e) => {
  if (e.target === navigation) {
    if (menuButton.classList.contains("visible")) {
      menuButton.classList.remove("visible");
      navigation.style.display = "none";
    } else {
      menuButton.classList.add("visible");
      navigation.style.display = "block";
    }

    lockScrollBody();
  }
});

// Open login modal when click login in header
const loginModal = document.querySelector("#login-modal");
const registerModal = document.querySelector("#register-modal");
const loginButton = document.querySelector(".header__login-button");

loginButton.addEventListener("click", (e) => {
  e.preventDefault();

  registerModal.style.display = "none";
  loginModal.style.display = "block";
});

// Open modals when click on link in modal__message
const openLoginModal = document.querySelector("#open-login-modal");
const openRegisterModal = document.querySelector("#open-register-modal");

openLoginModal.addEventListener("click", (e) => {
  e.preventDefault();
  registerModal.style.display = "none";
  loginModal.style.display = "block";
});

openRegisterModal.addEventListener("click", (e) => {
  e.preventDefault();
  loginModal.style.display = "none";
  registerModal.style.display = "block";
});

// Close modal when click close button
const closeRegisterModal = document.querySelector("#close-register-modal");
const closeLoginModal = document.querySelector("#close-login-modal");

closeRegisterModal.addEventListener("click", () => {
  registerModal.style.display = "none";
});

closeLoginModal.addEventListener("click", () => {
  loginModal.style.display = "none";
});

// Close modal when click outside modal
window.addEventListener("click", (e) => {
  if (e.target === loginModal || e.target === registerModal) {
    e.target.style.display = "none";
  }
});
