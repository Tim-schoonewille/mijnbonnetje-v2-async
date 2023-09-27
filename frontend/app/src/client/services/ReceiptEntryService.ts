/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ReceiptEntry } from '../models/ReceiptEntry';
import type { ReceiptEntryCreate } from '../models/ReceiptEntryCreate';
import type { ReceiptEntryUpdate } from '../models/ReceiptEntryUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ReceiptEntryService {

    /**
     * Create Receipt Entry
     * Create new receipt entry
     * Optional parameter: store_id (int | UUID)
     *
     * Raises:
     *
     * 404: {detail:"STORE_NOT_FOUND" }
     * @param requestBody
     * @returns ReceiptEntry Successful Response
     * @throws ApiError
     */
    public static receiptEntryCreateReceiptEntry(
        requestBody: ReceiptEntryCreate,
    ): CancelablePromise<ReceiptEntry> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/receipt-entry/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Multiple Receipt Entries
     * Retreive multiple receipt entries
     * (requires verifiied user token, or sudo token for all)
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns ReceiptEntry Successful Response
     * @throws ApiError
     */
    public static receiptEntryReadMultipleReceiptEntries(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<Array<ReceiptEntry>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/receipt-entry/',
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
     * Count Receipt Entries
     * Returns the amount of entries in DB.
     *
     * Can be filtered on a specific date in format: 'YYYY-MM-DD'.
     *
     * Custom filter can also be applied, but requires knowledge of the model.
     *
     *
     * Raises:
     *
     * 400: {detail: "DATE_FILTER_INVALID"}
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns any Successful Response
     * @throws ApiError
     */
    public static receiptEntryCountReceiptEntries(
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/receipt-entry/count',
            query: {
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
     * Read Specific Receipt Entry
     * Retreive a specific receipt entry (requires verifieduser token)
     *
     * Raises:
     *
     * 404: {detail="RECEIPT_ENTRY_NOT_FOUND"}
     * 403: {detail="NOT_YOUR_RECEIPT_ENTRY"}
     * @param receiptEntryId
     * @returns ReceiptEntry Successful Response
     * @throws ApiError
     */
    public static receiptEntryReadSpecificReceiptEntry(
        receiptEntryId: (number | string),
    ): CancelablePromise<ReceiptEntry> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/receipt-entry/{receipt_entry_id}',
            path: {
                'receipt_entry_id': receiptEntryId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Receipt Entry
     * update a specific receipt entry (requires verifieduser token)
     *
     * Raises:
     *
     * 404: {detail="RECEIPT_ENTRY_NOT_FOUND"}
     * 403: {detail="NOT_YOUR_RECEIPT_ENTRY"}
     * 404: {detail="STORE_NOT_FOUND"}
     * @param receiptEntryId
     * @param requestBody
     * @returns ReceiptEntry Successful Response
     * @throws ApiError
     */
    public static receiptEntryUpdateReceiptEntry(
        receiptEntryId: (number | string),
        requestBody: ReceiptEntryUpdate,
    ): CancelablePromise<ReceiptEntry> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/receipt-entry/{receipt_entry_id}',
            path: {
                'receipt_entry_id': receiptEntryId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Receipt Entry
     * delete a specific receipt entry (requires verifieduser token)
     *
     * Raises:
     *
     * 404: {detail="RECEIPT_ENTRY_NOT_FOUND"}
     * 403: {detail="NOT_YOUR_RECEIPT_ENTRY"}
     * @param receiptEntryId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static receiptEntryDeleteReceiptEntry(
        receiptEntryId: (number | string),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/receipt-entry/{receipt_entry_id}',
            path: {
                'receipt_entry_id': receiptEntryId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
