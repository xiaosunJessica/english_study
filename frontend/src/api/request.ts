// src/api/request.ts
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

const service = axios.create({
  baseURL: '/api', // 后端API地址
  timeout: 10000
});

// 请求拦截器
service.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
  },
  error => Promise.reject(error)
);

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => response.data,
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        // 处理未登录或token失效
      }
      // 其他错误处理
    }
    return Promise.reject(error);
  }
);

export default service;