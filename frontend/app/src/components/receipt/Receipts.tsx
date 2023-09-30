import React from "react";
import { ReceiptEntry, Store } from "../../client";
import TruncatedReceipt from "./TruncatedReceipt";
import { Box, Divider, SimpleGrid } from "@chakra-ui/react";

import { Link as NavLink } from "react-router-dom";

export type ReceiptsProps = {
  receipts: ReceiptEntry[] | null;
  stores: Store[] | null;
};

export default function Receipts({ receipts, stores }: ReceiptsProps) {
  if (!receipts) return <h1>No files...</h1>;
  return (
    <>
      <SimpleGrid
        maxWidth="1300px"
        columns={[1, 1, 2, 2]}
        spacingX="24px"
        spacingY="32px"
      >
        {receipts.map((receipt) => {
          const store = stores?.find((store) => store.id === receipt.storeId);
          return (
            <Box key={receipt.id}>
              <NavLink to={`/receipts/${receipt.id}`}>
                <TruncatedReceipt receipt={receipt} store={store} />
              </NavLink>
              <Divider visibility={["visible", "hidden"]} />
            </Box>
          );
        })}
      </SimpleGrid>
    </>
  );
}
