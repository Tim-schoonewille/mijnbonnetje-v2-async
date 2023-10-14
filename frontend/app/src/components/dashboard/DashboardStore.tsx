import {
  Box,
  Heading,
  Progress,
  Tab,
  Link as ChakraLink,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
  Button,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { ReceiptEntry, Store } from "../../client";
import { Link } from "react-router-dom";

type dashboardStoreProps = {
  stores: Store[];
  receipts: ReceiptEntry[];
  totalAmountMoney: number;
};

export default function DashboardStore({
  stores,
  receipts,
  totalAmountMoney,
}: dashboardStoreProps) {
  const [maxIterations, setMaxIterations] = useState(5);
  const storeTotalAmounts: { [key: string]: number } = {};
  const storeTotalQuantity: { [key: string]: number } = {};

  receipts.forEach((entry) => {
    const storeId = entry.storeId as string;
    const totalAmount = entry.totalAmount || 0; // Use 0 as default if totalAmount is missing

    if (storeId) {
      storeTotalAmounts[storeId] =
        (storeTotalAmounts[storeId] || 0) + totalAmount;
    }
  });

  receipts.forEach((entry) => {
    const storeId = entry.storeId as string;
    if (storeId) {
      storeTotalQuantity[storeId] = (storeTotalQuantity[storeId] || 0) + 1;
    }
  });

  const storesSortedByMoney = [...stores];
  const storesSortedByQuantity = [...stores];

  storesSortedByMoney.sort((storeA, storeB) => {
    const totalAmountA = storeTotalAmounts[storeA.id] || 0;
    const totalAmountB = storeTotalAmounts[storeB.id] || 0;

    return totalAmountB - totalAmountA;
  });

  storesSortedByQuantity.sort((storeA, storeB) => {
    const totalQuantityA = storeTotalQuantity[storeA.id] || 0;
    const totalQuantityB = storeTotalQuantity[storeB.id] || 0;

    return totalQuantityB - totalQuantityA;
  });

  return (
    <>
      {stores && (
        <Box m={5}>
          <Heading size="sm" mt={3} mb={3}>
            Stores:
          </Heading>

          <Tabs
            size="sm"
            isFitted
            variant="soft-rounded"
            p={0}
            m={0}
            mt={5}
            colorScheme="teal"
          >
            <Box maxH="250px" overflowY="auto">
              <TabPanels>
                <TabPanel>
                  {storesSortedByQuantity.map((store, i) => {
                    if (maxIterations && i >= maxIterations) return;
                    const total = receipts.length;
                    const percentage =
                      (storeTotalQuantity[store.id] / total) * 100;
                    return (
                      <>
                        <Link key={store.id} to={`/receipts?shop=${store.id}`}>
                          <Text mb={2}>{store.name.toLowerCase()}</Text>
                          <Progress
                            value={percentage}
                            size="sm"
                            colorScheme="teal"
                            rounded={6}
                            mb={2}
                          />
                        </Link>
                      </>
                    );
                  })}
                  <Button
                    variant="link"
                    mt={3}
                    onClick={() => setMaxIterations(maxIterations ? 0 : 5)}
                  >
                    {!maxIterations ? "less.." : "more..."}
                  </Button>
                </TabPanel>
                <TabPanel>
                  {storesSortedByMoney.map((store, i) => {
                    if (maxIterations && i >= maxIterations) return;

                    const percentage =
                      (storeTotalAmounts[store.id] / totalAmountMoney) * 100;
                    return (
                      <Link key={store.id} to={`/receipts?shop=${store.id}`}>
                        <Text mb={2}>{store.name.toLowerCase()}</Text>
                        <Progress
                          rounded={6}
                          mb={2}
                          value={percentage}
                          size="sm"
                          colorScheme="teal"
                        />
                      </Link>
                    );
                  })}

                  <Button
                    variant="link"
                    mt={3}
                    onClick={() => setMaxIterations(maxIterations ? 0 : 5)}
                  >
                    {!maxIterations ? "less.." : "more..."}
                  </Button>
                </TabPanel>
              </TabPanels>
            </Box>
            <TabList mt={3}>
              <Tab>Total</Tab>
              <Tab>MONEY</Tab>
            </TabList>
          </Tabs>
        </Box>
      )}
    </>
  );
}
