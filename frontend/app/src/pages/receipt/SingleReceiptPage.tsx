import { Flex, Spinner, Text } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ReceiptBody from "../../components/receipt/ReceiptBody";
import ProductItems from "../../components/receipt/ProductItems";
import ReceiptSummary from "../../components/receipt/ReceiptSummary";
import RequiresValidToken from "../../wrappers/RequiresValidToken";
import { useAuthContext } from "../../context/AuthContext";
import { Receipt, ReceiptService, Store, StoreService } from "../../client";

export default function SingleReceiptPage() {
  const { id } = useParams();
  const [receipt, setReceipt] = useState<Receipt>();
  const [stores, setStores] = useState<Store[]>();
  const receiptId = id || 0;
  const { isLoggedIn } = useAuthContext();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

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
  async function readReceipt() {
    try {
      setIsLoading(true);
      setError("");
      const response = await ReceiptService.receiptReadSpecificFullReceipt(
        receiptId
      );
      if (response.status === 200) {
        setReceipt(response.body);
      } else {
        setError("Error receiving receipt");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    if (!isLoggedIn) return;
    readReceipt();
    readStores();
  }, [isLoggedIn]);

  return (
    <RequiresValidToken>
      <Flex
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
        gap={15}
        mt="24px"
      >
        {!error ? (
          <ReceiptBody>
            {receipt && stores && (
              <ReceiptSummary receipt={receipt} stores={stores} />
            )}
            <ProductItems productItems={receipt?.productItems} />
          </ReceiptBody>
        ) : (
          <Text color={"red.400"}>{error}</Text>
        )}
        {isLoading && <Spinner />}
      </Flex>
    </RequiresValidToken>
  );
}
