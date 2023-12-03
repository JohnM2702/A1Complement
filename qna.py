import pickle
import random

class QuestionAnswerContainer:
    def __init__(self) -> None:
        self.qna_list = []

    def add_qna(self, new_qna:dict):
        """        
        {
            "q": "question/trivia",
            "a": "answer"
        }
        """
        self.qna_list.append(new_qna)

    def write_to_file(self):
        pickle_file = open('pickled_qna', 'ab')
        
        pickle.dump(self.qna_list, pickle_file)   

        pickle_file.close()

    def read_from_file(self):
        pickle_file = open('pickled_qna', 'rb')    

        extracted_qna_list = pickle.load(pickle_file)
        self.qna_list = extracted_qna_list

        pickle_file.close()

    def qna_list_dump(self):
        #- prints all qna and its corresponding index
        for index in range(len(self.qna_list)):
            print(f"{index}")
            print("q: " + str(self.qna_list[index]["q"]))
            print("a: " + str(self.qna_list[index]["a"]))
            print()
            
    def get_random_qna(self, number=1):
        if number > len(self.qna_list):
            print("Warning: The requested number is greater than the number of available Q&A pairs.")
            random.shuffle(self.qna_list)
            return self.qna_list


        random_qna_list = random.sample(self.qna_list, number)
        return random_qna_list

qna_obj = QuestionAnswerContainer()

qna_obj.add_qna(
  {
      "q": "What is the more scientific name for quicksilver?",
      "a": "Mercury"
  }
)

qna_obj.add_qna(
  {
      "q": "Of what continent is Cyprus a part?",
      "a": "Asia"
  }
)

qna_obj.add_qna(
  {
      "q": "What type of celestial body is Andromeda?",
      "a": "Galaxy"
  }
)

qna_obj.add_qna(
  {
      "q": "What country consumes the most fish per capita?",
      "a": "Japan"
  }
)

qna_obj.add_qna(
  {
      "q": "What is a Chorizo?",
      "a": "Spicy Sausage"
  }
)

qna_obj.add_qna(
  {
      "q": "What is Panphobia a fear of?",
      "a": "Everything"
  }
)

qna_obj.add_qna(
  {
      "q": "Crazy? I was crazy once. They locked me in a room. A rubber room with...",
      "a": "Rats"
  }
)

qna_obj.write_to_file()