/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ProductItem } from '../models/ProductItem';
import type { ProductItemCreate } from '../models/ProductItemCreate';
import type { ProductItemUpdate } from '../models/ProductItemUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ProductItemService {

    /**
     * Create Product Item
     * Create a product item, requires verified user token
     * @param requestBody
     * @returns ProductItem Successful Response
     * @throws ApiError
     */
    public static productItemCreateProductItem(
        requestBody: ProductItemCreate,
    ): CancelablePromise<ProductItem> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/product-item/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Multiple Product Items
     * Read multiple product items.
     * Query parameters for filters.
     * requires verified user otken
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
     * @returns ProductItem Successful Response
     * @throws ApiError
     */
    public static productItemReadMultipleProductItems(
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
    ): CancelablePromise<Array<ProductItem>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/product-item/',
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
     * Read Specific Product Item
     * Read specific product item in database.
     *
     * Raises:
     *
     * 404: {detail: " PRODUCT_ITEM_NOT_FOUND"}
     * 403: {detail: "ACCESS_DENIED" }
     * @param productItemId
     * @returns ProductItem Successful Response
     * @throws ApiError
     */
    public static productItemReadSpecificProductItem(
        productItemId: (number | string),
    ): CancelablePromise<ProductItem> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/product-item/{product_item_id}',
            path: {
                'product_item_id': productItemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Specific Product Item
     * Update specific product item in database.
     *
     * Raises:
     *
     * 404: {detail: " PRODUCT_ITEM_NOT_FOUND"}
     * 403: {detail: "ACCESS_DENIED" }
     * @param productItemId
     * @param requestBody
     * @returns ProductItem Successful Response
     * @throws ApiError
     */
    public static productItemUpdateSpecificProductItem(
        productItemId: (number | string),
        requestBody: ProductItemUpdate,
    ): CancelablePromise<ProductItem> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/product-item/{product_item_id}',
            path: {
                'product_item_id': productItemId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Specific Product Item
     * Delete specific product item in database.
     *
     * Raises:
     *
     * 404: {detail: " PRODUCT_ITEM_NOT_FOUND"}
     * 403: {detail: "ACCESS_DENIED" }
     * @param productItemId
     * @returns string Successful Response
     * @throws ApiError
     */
    public static productItemDeleteSpecificProductItem(
        productItemId: (number | string),
    ): CancelablePromise<Record<string, string>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/product-item/{product_item_id}',
            path: {
                'product_item_id': productItemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
