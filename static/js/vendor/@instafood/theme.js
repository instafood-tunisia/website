const storedPreference = localStorage.getItem('darkModePreference');

if (storedPreference) {
  setTheme(storedPreference);
}

function toggleTheme() {
  const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  setTheme(theme);
  localStorage.setItem('darkModePreference', theme);
 }

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
}

function colorTrace(msg, color) {
  console.log("%c" + msg, "color:" + color + ";font-weight:bold;");
}

colorTrace(atob("RGV2ZWxvcGVkIGJ5IEBha2F0aWdnZXJ4MDQgb24gZ2l0aHViLg=="), "green");

 