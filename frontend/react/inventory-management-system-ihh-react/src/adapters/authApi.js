export async function loginUser({ username, password }) {
  const formBody = new URLSearchParams({
    grant_type: 'password',
    username,
    password,
    scope: '',
    client_id: 'string',
    client_secret: '********', // Replace as needed
  });
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formBody,
  });
  return response;
}