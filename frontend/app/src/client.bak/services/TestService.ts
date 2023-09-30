/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TestService {

    /**
     * Mongo Request Limit Get
     * Test route te check wether the the amount of API requests is limited
     * @returns any Successful Response
     * @throws ApiError
     */
    public static testMongoRequestLimitGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/test/api-call-log-limit',
        });
    }

    /**
     * Read Collection
     * @param collection
     * @returns any Successful Response
     * @throws ApiError
     */
    public static testReadCollection(
        collection: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/test/get-collection',
            query: {
                'collection': collection,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Test Proxy
     * @param proxy
     * @returns any Successful Response
     * @throws ApiError
     */
    public static testTestProxy(
        proxy: string = '185.162.229.188:80',
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/test/test-proxy',
            query: {
                'proxy': proxy,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Test Proxy Cache Return
     * @returns any Successful Response
     * @throws ApiError
     */
    public static testTestProxyCacheReturn(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/test/test-proxy-cache-return',
        });
    }

    /**
     * Test Working Proxy List In Cache
     * @returns any Successful Response
     * @throws ApiError
     */
    public static testTestWorkingProxyListInCache(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/test/test-working-proxy-list-in-cache',
        });
    }

}
