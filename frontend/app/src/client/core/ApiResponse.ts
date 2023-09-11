export default interface ApiResponse<T>{
  body: object;
  ok: boolean;
  status: number;
  statusText: string;
  url: string;
}