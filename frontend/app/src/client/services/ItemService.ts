/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Item } from '../models/Item';
import type { ItemCreate } from '../models/ItemCreate';
import type { ItemUpdate } from '../models/ItemUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ItemService {

    /**
     * Read All Items
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns Item Successful Response
     * @throws ApiError
     */
    public static itemReadAllItems(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<Array<Item>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/item/',
            query: {
                'skip': skip,
                'limit': limit,
                'user_id': userId,
                'start_date': startDate,
                'end_date': endDate,
                'date_filter': dateFilter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create New Item
     * @param requestBody
     * @returns Item Successful Response
     * @throws ApiError
     */
    public static itemCreateNewItem(
        requestBody: ItemCreate,
    ): CancelablePromise<Item> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/item/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Specific Ite With Cache
     * @param itemId
     * @returns Item Successful Response
     * @throws ApiError
     */
    public static itemReadSpecificIteWithCache(
        itemId: (number | string),
    ): CancelablePromise<Item> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/item/{item_id}',
            path: {
                'item_id': itemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Specific Item
     * @param itemId
     * @param requestBody
     * @returns Item Successful Response
     * @throws ApiError
     */
    public static itemUpdateSpecificItem(
        itemId: (number | string),
        requestBody: ItemUpdate,
    ): CancelablePromise<Item> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/item/{item_id}',
            path: {
                'item_id': itemId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Specific Item
     * @param itemId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static itemDeleteSpecificItem(
        itemId: (number | string),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/item/{item_id}',
            path: {
                'item_id': itemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
