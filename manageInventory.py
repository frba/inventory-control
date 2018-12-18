# Concordia Genome Foundry
# Script create to manage a invetory
# author: Flavia Araujo
# date: november 19th, 2018
# use: python manageInventory.py <input file name> <output file name>


# imported packages
import sys
import sqlite3

# database
inventory = "in/inventory.db"
# open conexion with the db
localConn = sqlite3.connect(inventory)
localCursor = localConn.cursor()


def updateLocalDB(item):
    localCursor.execute("UPDATE data SET Volume = Volume-1 WHERE Item = '" + str(item) + "'")
    localConn.commit()


def verifyLocalDB(item):
    localCursor.execute("SELECT * FROM data WHERE Item = '" + str(item) + "'" + "AND Volume >= 1")
    result = localCursor.fetchall()
    return result


def verifyandmanipulateinvetory(itens):
    all_results = []
    # verify if all itens are available in the invetory
    for i in range(1, len(itens)):
        itens[i] = itens[i].strip()  # remove /n at the end of the word

        if itens[i] != '':
            result = verifyLocalDB(itens[i])

            # if the result from the db is empty print a warning
            if len(result) < 1:
                print "\033[1mWarning:\033[0m in " + '\033[1m' + str(
                    itens[0]) + '\033[0m' + " the item " + '\033[1m' + str(
                    itens[i]) + '\033[0m' + " is not available in the inventory"
                return None
            # Keep the result
            else:
                all_results.append(result)

    # All itens were found, so modify the quatity in the invetory
    for j in range(1, len(itens)):
        updateLocalDB(itens[j])

    return all_results


def selectitens(order):
    itens = []

    for i in range(0, len(order)):
        if order[i] == "":
            return itens
        else:
            itens.append(order[i])
    return itens


def readfile(path_in, path_out):

    filein = open(path_in, "r")
    fileout = open(path_out, "w")
    fileout.write("Order,Item,Shelf,Bin,Shipping Box,Volume\n")

    # jump header in input file
    for line in range(0, 4):
        header = filein.readline()
        # print filein.readline()

    # get each order and process it
    for line in filein:
        order = line.split(",")

        # verify and temporary store itens
        itens = selectitens(order)

        # verify if the itens are available in inventory
        results = verifyandmanipulateinvetory(itens)

        # get each result from the results
        if results != None:
             for result in results:
                shelf = result[0].__getitem__(1)
                bin = result[0].__getitem__(2)
                item = result[0].__getitem__(3)
                volume = result[0].__getitem__(4)
                num = int(filter(str.isdigit, str(itens[0])))

                #print output result in terminal
                print "\033[1m"+str(itens[0]) + "\033[0m"+ " : " + str(item) + "," + str(shelf) + "," + str(bin) + "," + "box_" + str(num) + "," + str(volume)

                #print result in output file
                fileout.write(str(itens[0]) + "," + str(item) + "," + str(shelf) + "," + str(bin) + "," + "box_" + str(num) + "," + str(volume) + "\n")

    fileout.close()
    filein.close()


def main():
    global localConn, localCursor

    if len(sys.argv) > 2:
        readfile(sys.argv[1], sys.argv[2])

    else:
        print "Insert the expected number of arguments"
        print "#Usage: python manageInventory.py input_file output_file\n"


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print 'Interrupted'
