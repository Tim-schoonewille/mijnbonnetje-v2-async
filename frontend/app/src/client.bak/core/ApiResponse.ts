export default interface ApiResponse<T>{
  body: T;
  ok: boolean;
  status: number;
  statusText: string;
  url: string;
}