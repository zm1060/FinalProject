import axios from 'axios'

const API_URL = process.env.API_URL || 'http://localhost:8080'

const axiosInstance = axios.create({
  baseURL: API_URL
})

export function setAuthToken(token) {
  axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}
export default axiosInstance
