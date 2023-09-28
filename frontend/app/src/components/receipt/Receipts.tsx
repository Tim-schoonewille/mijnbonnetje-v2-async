import React from "react";
import { ReceiptEntry } from "../../client";
import TruncatedReceipt from "./TruncatedReceipt";
import { SimpleGrid } from "@chakra-ui/react";

export type ReceiptsProps = {
  receipts: ReceiptEntry[] | null;
};

export default function Receipts({ receipts }: ReceiptsProps) {
  const foo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  return (
    <>
      <SimpleGrid maxWidth="1300px" columns={[1, 1, 2, 2]} spacingX="24px" spacingY='32px'>
        {foo.map((receipt) => {
          return <TruncatedReceipt />;
        })}
      </SimpleGrid>
    </>
  );
}
