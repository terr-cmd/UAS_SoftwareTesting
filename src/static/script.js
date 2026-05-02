// Cek apakah user sudah login, jika belum redirect ke halaman login
function cekLogin() {
  if (localStorage.getItem("isLoggedIn") !== "true") {
    window.location.href = "/";
  }
}

// Logout: hapus status login dan redirect ke halaman login
function logout() {
  localStorage.removeItem("isLoggedIn");
  window.location.href = "/";
}
