import request from './request';

export const getCorpusList = () => {
  return request({
    url: '/ApicorpusFly/fullList',
    method: 'get'
  });
};