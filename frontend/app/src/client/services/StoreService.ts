/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Store } from '../models/Store';
import type { StoreCreate } from '../models/StoreCreate';
import type { StoreUpdate } from '../models/StoreUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
import ApiResponse from '../core/ApiResponse';

export class StoreService {

    /**
     * Create Store
     * Creates a store (requires verified user token)
     * @param requestBody
     * @returns Store Successful Response
     * @throws ApiError
     */
    public static storeCreateStore(
        requestBody: StoreCreate,
    ): CancelablePromise<ApiResponse<any>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/store/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Multiple Stores
     * Returns a list of stores with parameter filter (requires verified user token)
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @param columnFilterString
     * @param columnFilterStringValue
     * @param columnFilterInt
     * @param columnFilterIntValue
     * @returns Store Successful Response
     * @throws ApiError
     */
    public static storeReadMultipleStores(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
        columnFilterString?: (string | null),
        columnFilterStringValue?: (string | null),
        columnFilterInt?: (string | null),
        columnFilterIntValue?: (number | null),
    ): CancelablePromise<ApiResponse<any>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/store/',
            query: {
                'skip': skip,
                'limit': limit,
                'user_id': userId,
                'start_date': startDate,
                'end_date': endDate,
                'date_filter': dateFilter,
                'column_filter_string': columnFilterString,
                'column_filter_string_value': columnFilterStringValue,
                'column_filter_int': columnFilterInt,
                'column_filter_int_value': columnFilterIntValue,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Store
     * Search for a store by parameter q (string) requires verified user token
     * @param q
     * @returns Store Successful Response
     * @throws ApiError
     */
    public static storeSearchStore(
        q: string,
    ): CancelablePromise<ApiResponse<any>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/store/search',
            query: {
                'q': q,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read User Stores
     * @returns Store Successful Response
     * @throws ApiError
     */
    public static storeReadUserStores(): CancelablePromise<ApiResponse<any>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: `/store/user?timestamp=${new Date().getTime()}`,
        });
    }

    /**
     * Read Specific Store
     * Reads a specific store from DB (requires verified user token)
     *
     * Raises:
     *
     * 404: {detail: "STORE_NOT_FOUND"}
     * @param storeId
     * @returns Store Successful Response
     * @throws ApiError
     */
    public static storeReadSpecificStore(
        storeId: (number | string),
    ): CancelablePromise<Store> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/store/{store_id}',
            path: {
                'store_id': storeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Store
     * Update specific store (requires sudo login)
     * c
     * Raises:
     *
     * 404: {detail: "STORE_NOT_FOUND"}
     * @param storeId
     * @param requestBody
     * @returns Store Successful Response
     * @throws ApiError
     */
    public static storeUpdateStore(
        storeId: (number | string),
        requestBody: StoreUpdate,
    ): CancelablePromise<Store> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/store/{store_id}',
            path: {
                'store_id': storeId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Store
     * delete specific store (requires sudo login)
     * c
     * Raises:
     *
     * 404: {detail: "STORE_NOT_FOUND"}
     * @param storeId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static storeDeleteStore(
        storeId: (number | string),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/store/{store_id}',
            path: {
                'store_id': storeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
