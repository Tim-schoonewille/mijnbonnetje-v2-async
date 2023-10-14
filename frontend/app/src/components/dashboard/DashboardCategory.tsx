import React, { useState } from "react";
import { ReceiptEntry } from "../../client";
import {
  Box,
  Button,
  Heading,
  Progress,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
} from "@chakra-ui/react";
import { AiOutlineConsoleSql } from "react-icons/ai";
import { Link } from "react-router-dom";

type dashboardCategoryProps = {
  categories: any;
  receipts: ReceiptEntry[];
  totalAmountMoney: number;
};
export default function DashboardCategory({
  categories,
  receipts,
  totalAmountMoney,
}: dashboardCategoryProps) {
  const [maxIterations, setMaxIterations] = useState(5);
  const categoryTotalAmounts: { [key: string]: number } = {};
  const categoryTotalQuantity: { [key: string]: number } = {};

  receipts.forEach((entry: ReceiptEntry) => {
    const category = entry.category as string;
    const totalAmount = entry.totalAmount || 0; // Use 0 as default if totalAmount is missing

    if (category) {
      categoryTotalAmounts[category] =
        (categoryTotalAmounts[category] || 0) + totalAmount;
    }
  });

  receipts.forEach((entry) => {
    const category = entry.category as string;
    if (category) {
      categoryTotalQuantity[category] =
        (categoryTotalQuantity[category] || 0) + 1;
    }
  });

  const categoriesSortedByMoney = [...categories];
  const categoriesSortedByQuantity = [...categories];

  categoriesSortedByMoney.sort((categoryA, categoryB) => {
    const totalAmountA = categoryTotalAmounts[categoryA] || 0;
    const totalAmountB = categoryTotalAmounts[categoryB] || 0;

    return totalAmountB - totalAmountA;
  });

  categoriesSortedByQuantity.sort((categoryA, categoryB) => {
    const totalQuantityA = categoryTotalQuantity[categoryA] || 0;
    const totalQuantityB = categoryTotalQuantity[categoryB] || 0;

    return totalQuantityB - totalQuantityA;
  });

  function countEntriesByCategory(
    entries: ReceiptEntry[] | null | undefined,
    categoryToCount: string
  ): number {
    if (!entries) return 0;
    const filteredEntries = entries.filter(
      (entry) => entry.category === categoryToCount
    );
    return filteredEntries.length;
  }

  function getTotalByCategory(
    entries: ReceiptEntry[] | null | undefined,
    categoryToCount: string
  ): number {
    if (!entries) return 0;
    const filteredEntries = entries.filter(
      (entry) => entry.category === categoryToCount
    );
    const totalAmount = filteredEntries.reduce((total, entry) => {
      return total + (entry.totalAmount || 0);
    }, 0);
    return totalAmount;
  }

  console.log('categories length: ', Object.keys(categoryTotalAmounts).length)

  return (
    <>
      <Box m={5}>
        <Heading size="sm" mt={3} mb={3}>
          Categories:
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
              <TabPanel mb={3}>
                {categoriesSortedByQuantity.map((category, i) => {
                  if (maxIterations && i >= maxIterations) return;
                  const totalPerCategory = countEntriesByCategory(
                    receipts,
                    category
                  );
                  if (totalPerCategory === 0) return;
                  const total = receipts.length;
                  const percentage =
                    (categoryTotalQuantity[category] / total) * 100;
                  console.log(category, percentage);
                  return (
                    <Box>
                      <Link

                        key={category}
                        to={`/receipts?category=${category}`}
                      >
                        <Text mb={2}>{category.toLowerCase()} ({categoryTotalQuantity[category]})</Text>
                        <Progress
                          value={
                            typeof percentage === "number" ? percentage : 0
                          }
                          size="sm"
                          colorScheme="teal"
                          rounded={6}
                          mb={4}
                        />
                      </Link>
                    </Box>
                  );
                })}
                {Object.keys(categoryTotalAmounts).length > maxIterations && (
                  <Button
                    variant="link"
                    mt={3}
                    onClick={() => setMaxIterations(maxIterations ? 0 : 5)}
                  >
                    {!maxIterations ? "less.." : "more..."}
                  </Button>
                )}
              </TabPanel>
              <TabPanel>
                {categoriesSortedByMoney.map((category, i) => {
                  if (maxIterations && i >= maxIterations) return;
                  const totalAmountPerCategory = getTotalByCategory(
                    receipts,
                    category
                  );
                  if (totalAmountPerCategory === 0) return;
                  console.log(category);
                  const percentage =
                    (categoryTotalAmounts[category] / totalAmountMoney) * 100;
                  return (
                    <>
                      <Link
                        key={category}
                        to={`/receipts?category=${category}`}
                      >
                        <Text mb={2}>{category.toLowerCase()} (€ {categoryTotalAmounts[category] /100 })</Text>
                        <Progress
                          value={
                            typeof percentage === "number" ? percentage : 0
                          }
                          size="sm"
                          colorScheme="teal"
                          rounded={6}
                          mb={2}
                        />
                      </Link>
                    </>
                  );
                })}
                {Object.keys(categoryTotalAmounts).length > maxIterations && (
                  <Button
                    variant="link"
                    mt={3}
                    onClick={() => setMaxIterations(maxIterations ? 0 : 5)}
                  >
                    {!maxIterations ? "less.." : "more..."}
                  </Button>
                )}
              </TabPanel>
            </TabPanels>
          </Box>
          <TabList mt={3}>
            <Tab>Total</Tab>
            <Tab>MONEY</Tab>
          </TabList>
        </Tabs>
      </Box>
    </>
  );
}
