export const login = async (username: string, password: string): Promise<string> => {
  const response = await fetch(`${process.env.REACT_APP_API_URL}/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: username,
      password: password,
    }),
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  const data = await response.json();
  return data.access_token; // JWTトークンを返す
};
