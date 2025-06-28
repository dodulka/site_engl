function getUsers() {
    return JSON.parse(localStorage.getItem('users') || '[]');
  }
  
  function saveUsers(users) {
    localStorage.setItem('users', JSON.stringify(users));
  }
  
  function getCurrentUser() {
    return localStorage.getItem('currentUser');
  }
  
  function setCurrentUser(username) {
    localStorage.setItem('currentUser', username);
  }
  
  function logout() {
    localStorage.removeItem('currentUser');
    location.href = 'login.html';
  }