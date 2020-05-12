import gpt_2_simple as gpt2
from sys import argv

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

single_text = gpt2.generate(sess, length=511, temperature=0.8, return_as_list=True, prefix=argv[1])

remDup = list(dict.fromkeys(single_text))
str1 = ''.join(remDup)

newstr = str1.replace("-", " ").replace("–"," ").replace("\n","").replace("  ", " ").replace(';','.')
res = newstr[:-3]
result = ''.join([i for i in newstr if not i.isdigit()])
print(result)

# remove numbers, add line breaks after each sentence ends and put to list, send list to VoiceCloner

text_file = open("configuration/text/result/final.txt", "w")
text_file.write(result)
text_file.close()