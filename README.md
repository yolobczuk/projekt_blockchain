"Blockchain project"

Main goal of this project is to learn how to build a simple blockchain in python.

# Initial requirements

* Backend - code that creates block and puts it into the simulated blockchain. It also should allow filling the block with data from Flask form.
* Flask - simple form that allows to save ticket data into the blockchain (such as name, surname, pesel [Polish unique identification number], value of ticket, penalty points given [if applicable] as well as name, surname and badge number of police officer that gave the ticket). All sensitive data such as names, surnames, PESEL and badge numbers will be hashed. It should give the possibility of showing tickets for given PESEL or badge number hash. It will also be convienient if the site would have the option to show hash for a specific PESEL/badge id. 
* Database - as it is expensive to put the data into a real blockchain network and it is hard to create your own network, my proposal is that we simulate the blockchain network by creating a conventional database that emulates the structure of blockchain.
