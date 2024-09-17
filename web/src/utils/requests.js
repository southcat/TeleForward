import axios from 'axios';
import { getToken, clearToken } from './token';
import { message } from 'antd';

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
});
const baseURLL = 'http://140.245.55.6:8000'


instance.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    // 将baseURL添加到请求的URL前，做替换http://127.0.0.1:8000 替换成baseURL
    config.url = config.url.replace("http://127.0.0.1:8000", baseURLL)
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      clearToken();
      if (typeof window !== 'undefined') {
        window.location.href = '/';
      }
      message.error('Token无效或已过期,请重新输入');
    } else {
      message.error(error.response?.data?.message || '发生错误,请稍后再试');
    }
    return Promise.reject(error);
  }
);

export const get = (url, params) => instance.get(url, { params });
export const post = (url, data) => instance.post(url, data);
export const put = (url, data) => instance.put(url, data);
export const del = (url) => instance.delete(url);

export default instance;
