/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_receipt_create_full_receipt } from "../models/Body_receipt_create_full_receipt";
import type { Receipt } from "../models/Receipt";

import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
import ApiResponse from "../core/ApiResponse";

export class ReceiptService {
  /**
   * Create Full Receipt
   * Creates a full receipt.
   * Intended for frontend to create a receipt from file.
   * Handles:
   *
   * Creating an entry
   *
   * Uploading a file
   *
   * ocr scan
   *
   * update the entry with store and product items
   *
   *
   * Raises:
   *
   * 400: {detail: "EXTERNAL_API_LIMIT_EXCEEDED}
   *
   * 400: {detail: "ERROR_IN_FILE"}
   *
   * 400: {detail: "FILE_TOO_LARGE_MAX_X_MB"}
   *
   * 400: {detail: "INVALID_FILE_TYPE}
   * @param formData
   * @param includeExternalOcr
   * @returns Receipt Successful Response
   * @throws ApiError
   */
  public static receiptCreateFullReceipt(
    formData: Body_receipt_create_full_receipt,
    includeExternalOcr: boolean = false
  ): CancelablePromise<Receipt> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/receipt/",
      query: {
        include_external_ocr: includeExternalOcr,
      },
      formData: formData,
      mediaType: "multipart/form-data",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Read Multiple Receipts
   * Read multiple receipts. Requires verified user token.
   * Parameter filters available
   * @param skip
   * @param limit
   * @param userId
   * @param startDate
   * @param endDate
   * @param dateFilter
   * @returns Receipt Successful Response
   * @throws ApiError
   */
  public static receiptReadMultipleReceipts(
    skip?: number,
    limit: number = 1000,
    userId?: number | string | null,
    startDate?: string | null,
    endDate?: string | null,
    dateFilter: string = "created_at"
  ): CancelablePromise<ApiResponse<any>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/receipt/",
      query: {
        skip: skip,
        limit: limit,
        user_id: userId,
        start_date: startDate,
        end_date: endDate,
        date_filter: dateFilter,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Read Specific Full Receipt
   * Retreive a full receipt from database with:
   * entry, file, scan, store?, product_items?
   *
   * Raises:
   *
   * 404: {detail:"RECEIPT_NOT_FOUND"}
   * 403: {detail: "ACCESS_DENIED"}
   * @param receiptId
   * @returns Receipt Successful Response
   * @throws ApiError
   */
  public static receiptReadSpecificFullReceipt(
    receiptId: number | string
  ): CancelablePromise<Receipt> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/receipt/{receipt_id}",
      path: {
        receipt_id: receiptId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Delete Specific Full Receipt
   * Delete a full receipt from database with:
   *
   * Raises:
   *
   * 404: {detail:"RECEIPT_NOT_FOUND"}
   * 403: {detail: "ACCESS_DENIED"}
   * @param receiptId
   * @returns any Successful Response
   * @throws ApiError
   */
  public static receiptDeleteSpecificFullReceipt(
    receiptId: number | string
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/receipt/{receipt_id}",
      path: {
        receipt_id: receiptId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
