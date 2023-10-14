import React, { useEffect, useState } from "react";
import RequiresValidToken from "../wrappers/RequiresValidToken";
import {
  Box,
  Button,
  Container,
  Divider,
  Flex,
  HStack,
  Heading,
  Icon,
  Progress,
  Spinner,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
  VStack,
} from "@chakra-ui/react";
import { LuLayoutDashboard } from "react-icons/lu";
import {
  Categories,
  ReceiptEntry,
  ReceiptEntryService,
  Store,
  StoreService,
} from "../client";
import { CopyIcon } from "@chakra-ui/icons";
import { RiMoneyDollarBoxLine } from "react-icons/ri";
import { Link } from "react-router-dom";
import DashboardStore from "../components/dashboard/DashboardStore";
import DashboardCategory from "../components/dashboard/DashboardCategory";

export default function DashboardPage() {
  const [receipts, setReceipts] = useState<ReceiptEntry[] | null>();
  const [isLoading, setIsLoading] = useState(false);
  const [showTotalAmount, setShowTotalAmount] = useState(false);
  const [showTotalAmountForStores, setShowTotalAmountForStores] = useState();
  const [stores, setStores] = useState<Store[] | null>();
  const [maxIStores, setMaxIStores] = useState(5);

  const categories = Object.values(Categories);

  async function getReceipts() {
    try {
      setIsLoading(true);
      const response =
        await ReceiptEntryService.receiptEntryReadMultipleReceiptEntries();
      if (response.status === 200) {
        setReceipts(response.body);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
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
    getReceipts();
    readStores();
  }, []);

  if (!receipts || !stores) return <></>;
  const dataLastSevenDays = processData("last7days");
  const dataLastMonth = processData("month");
  const dataLastYear = processData("year");
  const dataAll = processData("all");
  const totalAmountOfAllEntries = dataAll?.totalAmount
    ? dataAll.totalAmount
    : 9999;

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

  function getTotalByCategory(
    entries: ReceiptEntry[] | null | undefined,
    categoryToCount: string
  ): number {
    if (!entries) return 0;
    const filteredEntries = entries.filter(
      (entry) => entry.category === categoryToCount
    );
    const totalAmount = filteredEntries.reduce((total, entry) => {
      // Assuming each entry has a 'totalAmount' property
      return total + (entry.totalAmount || 0);
    }, 0);
    return totalAmount;
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
      {isLoading ? (
        <Spinner />
      ) : (
        <>
          <Flex
            justifyContent="center"
            alignItems="center"
            flexDirection="column"
            gap={15}
          >
            {dataLastSevenDays && dataLastMonth && dataLastYear && dataAll && (
              <Tabs
                w="100%"
                isFitted
                variant="enclosed"
                colorScheme="teal"
                mb={0}
              >
                <TabList>
                  <Tab>7-days</Tab>
                  <Tab>month</Tab>
                  <Tab>year</Tab>
                  <Tab>all</Tab>
                </TabList>

                <TabPanels>
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
                          lastSevenDaysStartDate
                        )}`}
                      >
                        <Button mt={5} variant="outline" w="100%">
                          Show selection
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
                        <Text as="i">€ {dataLastMonth.totalAmount / 100}</Text>
                      </HStack>
                      <Link
                        to={`/receipts?startDate=${formatDate(
                          currentMonthStartDate
                        )}`}
                      >
                        <Button mt={5} variant="outline" w="100%">
                          Show selection
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
                        <Button mt={5} variant="outline" w="100%">
                          Show selection
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
                        <Button mt={5} variant="outline" w="100%">
                          Show selection
                        </Button>
                      </Link>
                    </Box>
                  </TabPanel>
                </TabPanels>
              </Tabs>
            )}
          </Flex>
          <Divider mt={3} mb={10} />
          {dataAll && (
            <DashboardCategory
              categories={categories}
              receipts={receipts}
              totalAmountMoney={dataAll.totalAmount}
            />
          )}
          <Divider mt={3} mb={10} />
          {stores && dataAll && (
            <DashboardStore
              stores={stores}
              receipts={receipts}
              totalAmountMoney={dataAll.totalAmount}
            />
          )}
        </>
      )}
    </RequiresValidToken>
  );
}
