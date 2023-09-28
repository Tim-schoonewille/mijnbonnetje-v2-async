import React from "react";
import { ReceiptEntry } from "../../client";
import TruncatedReceipt from "./TruncatedReceipt";
import { Box, Divider, SimpleGrid } from "@chakra-ui/react";

import { Link as NavLink } from "react-router-dom";

export type ReceiptsProps = {
  receipts: ReceiptEntry[] | null;
};

export default function Receipts({ receipts }: ReceiptsProps) {
  const foo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  return (
    <>
      <SimpleGrid
        maxWidth="1300px"
        columns={[1, 1, 2, 2]}
        spacingX="24px"
        spacingY="32px"
      >
        {foo.map((receipt) => {
          return (
            <Box>
              <NavLink to={`/receipts/${receipt}`}>
                <TruncatedReceipt />
              </NavLink>
              <Divider visibility={["visible", "hidden"]} />
            </Box>
          );
        })}
      </SimpleGrid>
    </>
  );
}
