/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_receipt_file_create_receipt_file } from '../models/Body_receipt_file_create_receipt_file';
import type { ReceiptFile } from '../models/ReceiptFile';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ReceiptFileService {

    /**
     * Create Receipt File
     * Upload a receipt to server.
     *
     * Raises:
     *
     * 400: {detail: "ERROR_IN_FILE"}
     *
     * 400: {detail: "FILE_TOO_LARGE_MAX_X_MB"}
     *
     * 400: {detail: "INVALID_FILE_TYPE}
     * @param entryId
     * @param formData
     * @returns ReceiptFile Successful Response
     * @throws ApiError
     */
    public static receiptFileCreateReceiptFile(
        entryId: (number | string),
        formData: Body_receipt_file_create_receipt_file,
    ): CancelablePromise<ReceiptFile> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/receipt-file/',
            query: {
                'entry_id': entryId,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Multiple Receipt Files
     * Return multiple receipt files, depending on given parameters
     * Requires verified user token
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
     * @returns ReceiptFile Successful Response
     * @throws ApiError
     */
    public static receiptFileReadMultipleReceiptFiles(
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
    ): CancelablePromise<Array<ReceiptFile>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/receipt-file/',
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
     * Read Specific Receipt File
     * Returns specific receipt file from database, requires verified user token
     *
     * Raises:
     *
     * 403: {detail: "NOT_YOUR_RECEIPT_FILE"}
     *
     * 404: {detail: "RECEIPT_FILE_NOT_FOUND"}
     * @param receiptFileId
     * @returns ReceiptFile Successful Response
     * @throws ApiError
     */
    public static receiptFileReadSpecificReceiptFile(
        receiptFileId: (number | string),
    ): CancelablePromise<ReceiptFile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/receipt-file/{receipt_file_id}',
            path: {
                'receipt_file_id': receiptFileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Receipt File
     * deeletes a specific receipt file from database, requires verified user token
     *
     * Raises:
     *
     * 403: {detail: "NOT_YOUR_RECEIPT_FILE"}
     *
     * 404: {detail: "RECEIPT_FILE_NOT_FOUND"}
     *
     * 404: {detail: "RECEIPT_IMAGE_NOT_FOUND"}
     * @param receiptFileId
     * @returns string Successful Response
     * @throws ApiError
     */
    public static receiptFileDeleteReceiptFile(
        receiptFileId: (number | string),
    ): CancelablePromise<Record<string, string>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/receipt-file/{receipt_file_id}',
            path: {
                'receipt_file_id': receiptFileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
