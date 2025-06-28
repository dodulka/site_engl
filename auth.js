function register(username, password) {
    const users = getUsers();
    if (users.find(u => u.username === username)) {
      return 'Користувач з таким ім’ям вже існує';
    }
    users.push({ username, password, learned: [] });
    saveUsers(users);
    return null;
  }
  
  function login(username, password) {
    const users = getUsers();
    const user = users.find(u => u.username === username && u.password === password);
    if (user) {
      setCurrentUser(user.username);
      return true;
    }
    return false;
  }
  