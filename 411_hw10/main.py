import sys
import numpy
import json


# this function calculates entrophy
# takes input array of yes/no
def calculate_entrophy(input):
    x, unique_count = numpy.unique(input, return_counts=True)
    probabilities = unique_count/len(input)
    total = 0
    for i in probabilities:
        if(i != 0):
            total += (i * numpy.log2(i) * -1)
    return total

# DECISION TREE IMPLEMENTATION
def learn_decision_tree(examples, attributes, output, parent_examples):
  
    # if examples is empty then return plurality-value
    # selects the most common output value
    if(len(examples) == 0):
        val, count = numpy.unique(output, return_counts=True)
        plurality_value = val[numpy.argmax(count)]
        return plurality_value
  
    # if all examples have the same classification then return the classification
    # classification = len(numpy.unique(output))
  
    elif(len(numpy.unique(output)) == 1):
        return output[0]

    # if attributes is empty then return plurality-value
    # selects the most common output value
    elif(len(attributes) == 0):
        val, count = numpy.unique(output, return_counts=True)
        plurality_value = val[numpy.argmax(count)]
        return plurality_value

    # 
    else:
        # variables
        tree = {}
        example2 = []
        attribtues2 = []
        output2 = []
        list_val = []
        A = []

        # creates an array
        example = numpy.array(examples)
 #      [['Yes' 'No' 'No' '$' 'No' 'No' '30-60']
 # ['Yes' 'No' 'Yes' '$' 'No' 'No' '10-30']]
        # print(example)
        # access attribute  
        attribute_example = example.T
        # print(attribute_example)
 #      [['Yes' 'Yes']
 # ['No' 'No']
 # ['No' 'Yes']
 # ['$' '$']
 # ['No' 'No']
 # ['No' 'No']
 # ['30-60' '10-30']]





        # INFORMATION GAIN CALCULATION
        for i in attribute_example:
          result = calculate_entrophy(output)
          parsed_example, unique_count = numpy.unique(i, return_counts=True)
          probabilities = unique_count/len(i)
          
          for j in range(0, len(parsed_example)):
              temp2 = []
              for index in range(0, len(i)):
                  if(i[index] == parsed_example[j]):
                      temp2.append(output[index])
              result += (-1 * probabilities[j] * calculate_entrophy(temp2))


          num = round(result, 3)
          # print(num)
          list_val.append(num)

        # print(list_val)
        # [0.0, 0.0, 0.021, 0.196, 0.541, 0.196, 0.0, 0.021, 0.0, 0.208]
        # [0.109, 0.0, 0.109, 0.252, 0.252, 0.109, 0.252, 0.252, 0.252]
        # [0.0, 0.0, 0.311, 0.311, 0.0, 0.311, 0.5, 0.0]
        # [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

        argmax = numpy.argwhere(list_val == numpy.amax(list_val))
      
        # returns attribute specific array idx,val
        attribute = example[:, argmax[0][0]]
        v = numpy.unique(attribute)
        for value in v:
            A.append({"attribute": value, "pos": (attribute == value).nonzero()[0]})
    
        # RECURSIVELY SPLIT DATASET
        for each in A:
          
#         print(A)
#       [{'attribute': 'Full', 'pos': array([ 1,  3,  4,  8,  9, 11])},
            cur = argmax[0][0]
            example2 = numpy.delete(example.take(each["pos"], axis=0), cur, 1).tolist()
            attributes2 = attributes[:cur] + attributes[cur+1:]
            output2 = numpy.array(output).take(each["pos"], axis=0).tolist()  
            subTree = attributes[cur] + each["attribute"]
            tree[subTree] = learn_decision_tree(example2, attributes2, output2, parent_examples)
        
        return tree;



def main():

  # variables
  given = []
  parent_examples = []
  examples = []
  attributes = ["Other Options?", 
                "Restaurant2?", 
                "Fri/Sat?", 
                "Hungry?", 
                "Patrons?", 
                "Price?", 
                "Raining?", 
                "Reservation?", 
                "Type?", 
                "Wait Time?"]

  # open, read and parse from file
  filename = sys.argv[1] 
#   filename = "restaurant.csv"
  
  f = open(filename, 'r')
  for each in f:
    words = each.split(',')
    given.append([i.strip() for i in words])

  for each in given:
    parent_examples.append(each[-1])
    
  for each in given:
    examples.append(each[0:-1])
  
  # call decision tree
  decisionTree = learn_decision_tree(examples, attributes, parent_examples, parent_examples)
  # PRINT THE RESULTING DECISION TREE
  print(decisionTree)


if __name__ == "__main__":
    main()