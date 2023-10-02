import { Accordion, Box, Flex, Spinner } from "@chakra-ui/react";

import ReceiptFilterMenu from "../../components/receipt/ReceiptFilterMenu";
import ReceiptOrderByMenu from "../../components/receipt/ReceiptOrderByMenu";
import { useEffect, useRef, useState } from "react";
import Receipts from "../../components/receipt/Receipts";
import {
  ReceiptEntry,
  ReceiptEntryService,
  Store,
  StoreService,
} from "../../client";
import RequiresValidToken from "../../wrappers/RequiresValidToken";
import { useSearchParams } from "react-router-dom";

export default function ReceiptsPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [receipts, setReceipts] = useState<ReceiptEntry[] | null>(null);
  const [stores, setStores] = useState<Store[] | null>(null);
  const [filter, setFilter] = useState("");
  const [queryParams] = useSearchParams();

  const orderBy = queryParams.get("orderBy") || undefined;
  const sort = queryParams.get("sort") || undefined;
  const categoryParam = queryParams.get("category") || undefined;
  const storeParam = queryParams.get("shop") || undefined;

  async function readReceipts() {
    let payload = {};
    if (categoryParam) {
      payload = {
        ...payload,
        columnFilterStringValue: categoryParam,
        columnFilterString: "category",
      };
    }
    if (storeParam) {
      console.log("has store param");
      const StoreFromParam = stores?.find((store) => store.name === storeParam);
      payload = {
        ...payload,
        columnFilterIntValue: StoreFromParam?.id,
        columnFilterInt: "store_id",
      };
    }
    try {
      console.log(payload);
      const response =
        await ReceiptEntryService.receiptEntryReadMultipleReceiptEntries(
          payload
        );

      setReceipts(response.body);
    } catch (e) {
      console.error(e);
    }
  }
  async function readStores() {
    try {
      setIsLoading(true);
      const response = await StoreService.storeReadUserStores();
      if (response.status === 200) {
        setStores(response.body);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }
  useEffect(() => {
    readReceipts();
    readStores();
  }, [categoryParam, storeParam]);

  if (orderBy && receipts && sort) {
    switch (orderBy) {
      case "money":
        switch (sort) {
          case "asc":
            receipts?.sort(
              (a, b) => (a.totalAmount || 0) - (b.totalAmount || 0)
            );
            break;
          case "desc":
            receipts?.sort(
              (a, b) => (b.totalAmount || 0) - (a.totalAmount || 0)
            );
            break;
          default:
            break;
        }
        break;
      case "date":
        switch (sort) {
          case "asc":
            receipts?.sort(
              (a, b) =>
                new Date(a.purchaseDate).getTime() -
                new Date(b.purchaseDate).getTime()
            );
            break;
          case "desc":
            receipts?.sort(
              (a, b) =>
                new Date(b.purchaseDate).getTime() -
                new Date(a.purchaseDate).getTime()
            );
            break;
          default:
            break;
        }
        break;
      default:
        break;
    }
  }

  console.log(receipts);
  return (
    <RequiresValidToken>
      <Accordion allowToggle>
        <ReceiptFilterMenu stores={stores} />
        <ReceiptOrderByMenu />
      </Accordion>

      <Flex
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
        gap={15}
        mt="24px"
      >
        <Receipts receipts={receipts} stores={stores} />
        {isLoading && <Spinner />}
      </Flex>
    </RequiresValidToken>
  );
}
