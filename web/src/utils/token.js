// 用于存储token的key
const TOKEN_KEY = 'auth_token';

// 设置token
export const setToken = (token) => {
  localStorage.setItem(TOKEN_KEY, token);
};

// 获取token
export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

// 清除token 
export const clearToken = () => {
  localStorage.removeItem(TOKEN_KEY);
};

// 检查是否有token
export const hasToken = () => {
  return !!getToken();
};
