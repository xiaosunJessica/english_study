import request from './request';

export const getCorpusList = () => {
  return request({
    url: '/ApicorpusFly/fullList',
    method: 'get'
  });
};

export const getCorpusItem = (params: {
  book_id: number,
  unit_id: number,
  lesson_id: number,
}) => {
  return request({
    url: '/ApicorpusFly/fullItem',
    method: 'get',
    params: params
  });
};