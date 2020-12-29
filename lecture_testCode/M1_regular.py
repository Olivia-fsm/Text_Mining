import re
# import string

def test(StrList):
    return [w for w in StrList if w.endswith('s')]

def regTest(text):
    return re.findall(r'(?:\d{2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{2},? )?\d{4}', text)

if __name__ == "__main__":
    # testList=[]
    # for i in range(10):
    #     user_input = input("Input the next string:")
    #     testList.append(user_input)
    # print(test(testList))

    # text1 = "ouagadougou"
    # testList1_1=text1.split('ou')
    # testList1_2=text1.rsplit('ou')
    # print("testList1_1:", testList1_1)
    # print("testList1_2:", testList1_2)
    # print(",".join(testList1_1))
    # print("ou".join(testList1_2))
    textList = ["October 23, 2002", "23 Oct 2002", "23 October 2002", "Oct 23, 2002", "October 23 2002"]
    output = [regTest(text) for text in textList]
    print(output)
