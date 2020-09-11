package main

import (
	"flag"
	"fmt"

	github.com/domainr/whois
	"github.com/piotrszlenk/ssl-test/pkg/logz"
)

func main() {
	var logger *logz.LogHandler

	// Parse CLI arguments
	ipFile := flag.String("ip-file", "ips.txt", "Flat file with list of IPs")
	debugFlag := flag.Bool("debug", false, "Enable debug logging.")

	flag.Parse()
	logger = logz.InitLog(debugFlag)

	logger.Debug.Println("Command line arguments: ")
	logger.Debug.Println(" -p-file set to:", *ipFile)
	logger.Debug.Println(" -debug set to:", *debugFlag)

	result, err := whois.Whois("1.1.1.1")
	if err == nil {
		fmt.Println(result)
	}
	//	// Create list of ips
	//	logger.Info.Println("Loading IPs from:", *ipFile)
	//	ip_list := endpoint.NewIPs(*endpointFile)
	//	_, err := endpoints.LoadEndpoints()
	//	if err != nil {
	//		logger.Error.Fatalln(err)
	//	}
	//
	//	//Create test targets
	//	logger.Info.Println("Creating test targets from loaded endpoints.")
	//	testtargets := certcheck.NewTestTargets(endpoints, caPath)
	//	testtargets.Test()
	//	testtargets.PrintResults()
	//	//logger.Debug.Print(testtargets)
}
