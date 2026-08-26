const SECRET_PASS = "123456";

const authForm = document.querySelector('#dashboard-auth-form');
const passwordInput = document.querySelector('#dashboard-password');
const authError = document.querySelector('#dashboard-auth-error');
const dashboardContent = document.querySelector('.dashboard-content');
const lockButton = document.querySelector('#lock-dashboard');

const setAuthenticated = (authenticated) => {
  document.body.classList.toggle('dashboard-unlocked', authenticated);
  dashboardContent.setAttribute('aria-hidden', String(!authenticated));
  if (!authenticated) {
    passwordInput.value = '';
    authError.hidden = true;
    passwordInput.focus();
  }
};

authForm.addEventListener('submit', (event) => {
  event.preventDefault();
  if (passwordInput.value !== SECRET_PASS) {
    authError.hidden = false;
    passwordInput.select();
    return;
  }

  setAuthenticated(true);
  document.dispatchEvent(new CustomEvent('dashboard-authenticated'));
});

lockButton.addEventListener('click', () => {
  setAuthenticated(false);
});

setAuthenticated(false);
