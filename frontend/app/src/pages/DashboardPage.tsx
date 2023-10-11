import React, { useEffect, useState } from "react";
import RequiresValidToken from "../wrappers/RequiresValidToken";
import {
  Box,
  Button,
  Divider,
  Flex,
  HStack,
  Heading,
  Icon,
  Progress,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
  VStack,
} from "@chakra-ui/react";
import { LuLayoutDashboard } from "react-icons/lu";
import { Categories, ReceiptEntry, ReceiptEntryService } from "../client";
import { CopyIcon } from "@chakra-ui/icons";
import { RiMoneyDollarBoxLine } from "react-icons/ri";
import { Link } from "react-router-dom";

export default function DashboardPage() {
  const [receipts, setReceipts] = useState<ReceiptEntry[] | null>();
  const [isLoading, setIsLoading] = useState(false);

  const categories = Object.values(Categories);

  async function getReceipts() {
    try {
      setIsLoading(true);
      const response =
        await ReceiptEntryService.receiptEntryReadMultipleReceiptEntries();
      if (response.status === 200) {
        setReceipts(response.body);
        console.log(response.body);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    getReceipts();
  }, []);

  const dataLastSevenDays = processData("last7days");
  const dataLastMonth = processData("month");
  const dataLastYear = processData("year");
  const dataAll = processData("all");

  // Function to process data based on the selected filter
  function processData(selectedFilter: string) {
    if (!receipts) return;
    const filteredReceipts = receipts.filter((receipt) => {
      const purchaseDate = new Date(receipt.purchaseDate);

      switch (selectedFilter) {
        case "last7days":
          const sevenDaysAgo = new Date();
          sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
          return purchaseDate >= sevenDaysAgo;
        case "month":
          const startOfMonth = new Date();
          startOfMonth.setDate(1);
          startOfMonth.setHours(0, 0, 0, 0);
          return purchaseDate >= startOfMonth;
        case "year":
          const startOfYear = new Date();
          startOfYear.setMonth(0, 1);
          startOfYear.setHours(0, 0, 0, 0);
          return purchaseDate >= startOfYear;
        default:
          return true; // 'all' filter, include all receipts
      }
    });

    const totalReceipts = filteredReceipts.length;
    const totalAmount = filteredReceipts.reduce(
      (total, receipt) =>
        total + (receipt.totalAmount ? receipt.totalAmount : 0),
      0
    );

    return {
      totalReceipts,
      totalAmount,
    };
  }

  // Now you have four objects representing the outcome of each filter
  console.log("last seven days:", dataLastSevenDays);
  console.log("last month", dataLastMonth);
  console.log("last year", dataLastYear);
  console.log("all", dataAll);

  const lastSevenDaysStartDate = new Date();
  lastSevenDaysStartDate.setDate(lastSevenDaysStartDate.getDate() - 7);

  const currentMonthStartDate = new Date();
  currentMonthStartDate.setDate(1);

  const currentYearStartDate = new Date();
  currentYearStartDate.setMonth(0, 1);

  function formatDate(date: Date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

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
  return (
    <RequiresValidToken>
      {/* <HStack p={5}>
        <Icon as={LuLayoutDashboard} />
        <Heading size={"md"}>Dashboard</Heading>
      </HStack>

      <Heading size="sm" p={3} pl={5}>
        stats:
      </Heading> */}
      <Flex
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
        gap={15}
      >
        {dataLastSevenDays && dataLastMonth && dataLastYear && dataAll && (
          <Tabs w="100%" isFitted variant="enclosed">
            <TabList>
              <Tab>7-days</Tab>
              <Tab>month</Tab>
              <Tab>year</Tab>
              <Tab>all</Tab>
            </TabList>

            <TabPanels pl={5} pt={3}>
              <TabPanel>
                <Box>
                  <HStack>
                    <CopyIcon />
                    <Text fontWeight="bold">Total Receipts:</Text>
                    <Text>{dataLastSevenDays.totalReceipts}</Text>
                  </HStack>
                  <HStack>
                    <Icon as={RiMoneyDollarBoxLine} />
                    <Text fontWeight="bold">Total Amount:</Text>
                    <Text>€ {dataLastSevenDays.totalAmount / 100}</Text>
                  </HStack>
                  <Link
                    to={`/receipts?startDate=${formatDate(
                      currentMonthStartDate
                    )}`}
                  >
                    <Button mt={5} variant="ghost">
                      Show receipts
                    </Button>
                  </Link>
                </Box>
              </TabPanel>
              <TabPanel>
                <Box>
                  <HStack>
                    <CopyIcon />
                    <Text fontWeight="bold">Total Receipts:</Text>
                    <Text>{dataLastMonth.totalReceipts}</Text>
                  </HStack>
                  <HStack>
                    <Icon as={RiMoneyDollarBoxLine} />
                    <Text fontWeight="bold">Total Amount:</Text>
                    <Text>€ {dataLastMonth.totalAmount / 100}</Text>
                  </HStack>
                  <Link
                    to={`/receipts?startDate=${formatDate(
                      currentYearStartDate
                    )}`}
                  >
                    <Button mt={5} variant="ghost">
                      Show receipts
                    </Button>
                  </Link>
                </Box>
              </TabPanel>
              <TabPanel>
                <Box>
                  <HStack>
                    <CopyIcon />
                    <Text fontWeight="bold">Total Receipts:</Text>
                    <Text>{dataLastYear.totalReceipts}</Text>
                  </HStack>
                  <HStack>
                    <Icon as={RiMoneyDollarBoxLine} />
                    <Text fontWeight="bold">Total Amount:</Text>
                    <Text>€ {dataLastYear.totalAmount / 100}</Text>
                  </HStack>
                  <Link
                    to={`/receipts?startDate=${formatDate(
                      currentYearStartDate
                    )}`}
                  >
                    <Button mt={5} variant="ghost">
                      Show receipts
                    </Button>
                  </Link>
                </Box>
              </TabPanel>
              <TabPanel>
                <Box>
                  <HStack>
                    <CopyIcon />
                    <Text fontWeight="bold">Total Receipts:</Text>
                    <Text>{dataAll.totalReceipts}</Text>
                  </HStack>
                  <HStack>
                    <Icon as={RiMoneyDollarBoxLine} />
                    <Text fontWeight="bold">Total Amount:</Text>
                    <Text>€ {dataAll.totalAmount / 100}</Text>
                  </HStack>
                  <Link to="/receipts">
                    <Button mt={5} variant="ghost">
                      Show receipts
                    </Button>
                  </Link>
                </Box>
              </TabPanel>
            </TabPanels>
          </Tabs>
        )}
      </Flex>
      <Divider mt={3} mb={3} />
      <Box m={5}>
        <Heading size="sm" mb={3}>
          Total per category:
        </Heading>
        {categories.map((category) => {
          const totalEntriesInCategory = countEntriesByCategory(
            receipts,
            category
          );
          const totalEntries = receipts ? receipts.length : 100;
          const percentageofEntries =
            (totalEntriesInCategory / totalEntries) * 100;
          if (totalEntriesInCategory === 0) return;
          return (
            <Link to={`/receipts/?category=${category}`}>
              <Flex flexDirection={"column"} mb={2}>
                <Text mb={1}>
                  {category} ({totalEntriesInCategory})
                </Text>
                <Progress
                  size="sm"
                  colorScheme="teal"
                  value={percentageofEntries}
                />
              </Flex>
            </Link>
          );
        })}
      </Box>
    </RequiresValidToken>
  );
}
