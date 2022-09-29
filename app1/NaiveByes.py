from googletrans import Translator
from nltk.corpus import stopwords
import snscrape.modules.twitter as sntwitter
import string, copy
import nltk
from numerize import numerize

nltk.download('stopwords')
translator = Translator()


# Extract actual necessary words from the tweet
def extract_tweet_words(tweet_words):
    words = []
    alpha_lower = string.ascii_lowercase
    alpha_upper = string.ascii_uppercase
    numbers = [str(n) for n in range(10)]
    for word in tweet_words:
        cur_word = ''
        for c in word:
            if (c not in alpha_lower) and (c not in alpha_upper) and (c not in numbers):
                if len(cur_word) >= 2:
                    words.append(cur_word.lower())
                cur_word = ''
                continue
            cur_word += c
        if len(cur_word) >= 2:
            words.append(cur_word.lower())
    return words


def extract_words(tweet_words):
    words = []
    alpha_lower = string.ascii_lowercase
    alpha_upper = string.ascii_uppercase
    numbers = [str(n) for n in range(10)]
    for word in tweet_words:
        cur_word = ''
        for c in word:
            if (c not in alpha_lower) and (c not in alpha_upper) and (c not in numbers):
                if len(cur_word) >= 2:
                    words.append(cur_word.lower())
                cur_word = ''
                continue
            cur_word += c
        if len(cur_word) >= 2:
            words.append(cur_word.lower())
    return words

# Get Training Data from the input file


def get_tweet_training_data():
    here = path.abspath(path.dirname(__file__))
    f = open(path.join(here, 'training.txt'), 'r', encoding='utf-8')
    training_data = []
    for l in f.readlines():
        l = l.strip()
        tweet_details = l.split()

        tweet_label = tweet_details[0]
        tweet_words = extract_tweet_words(tweet_details[1:])
        training_data.append([tweet_label, tweet_words])

    f.close()

    return training_data

# Get Test Data from the input file


def splitAll(str):
    str = str.replace('\n', '')
    str = str.split(' ')
    return str


def get_tweet_test_data(username, quantity):

    query = '(from:{})'.format(username)
    validation_data = []
    obj = {
        'tweets': [],
    }
    tempTweet = {
        'date': '',
        'month': '',
        'content': '',
        'comments': '',
        'retweets': '',
        'likes': ''
    }
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if (i == 0):
            obj['profileImage'] = tweet.user.profileImageUrl
            obj['displayname'] = tweet.user.displayname
            obj['username'] = tweet.user.username
            obj['mediaCount'] = numerize.numerize(tweet.user.mediaCount)
            obj['cmonth'] = tweet.user.created.strftime('%b')
            obj['cyear'] = tweet.user.created.year
            obj['followersCount'] = numerize.numerize(tweet.user.followersCount)
            obj['friendsCount'] = numerize.numerize(tweet.user.friendsCount)
            obj['location'] = tweet.user.location
            obj['linkUrl'] = 'https://twitter.com/{}'.format(username)
        actualTweet = temp = ' '.join(word for word in splitAll(
            tweet.content) if not word.startswith('https:'))
        temp = (translator.translate(temp, dest='en')).text
        tempTweet.update({'content':  copy.deepcopy(actualTweet)})
        tempTweet.update({'date': tweet.date.day})
        tempTweet.update({'month': tweet.date.strftime('%b')})
        tempTweet.update({'comments': tweet.replyCount})
        tempTweet.update({'retweets': tweet.retweetCount})
        tempTweet.update({'likes': tweet.likeCount})
        obj.get('tweets').append([copy.deepcopy(tempTweet)])
        # ---------------------------- R e m o v e   S t o p   W o r d s ---------------------------
        temp = ' '.join([word for word in temp.split()
                        if word not in stopwords.words("english")])
        tweet_words = extract_words(temp.split())
        validation_data.append(['', tweet_words, actualTweet])
        if (i == quantity-1):
            break
    else:
        return 0

    return (validation_data, obj)

# Get list of words in the training data


def get_words(training_data):
    words = []
    for data in training_data:
        words.extend(data[1])
    return list(set(words))

# Get Probability of each word in the training data
# If label is specified, find the probability of each word in the corresponding labelled tweets only


def get_tweet_word_prob(training_data, label=None):
    words = get_words(training_data)
    freq = {}

    for word in words:
        freq[word] = 1

    total_count = 0
    for data in training_data:
        if data[0] == label or label == None:
            total_count += len(data[1])
            for word in data[1]:
                freq[word] += 1
    prob = {}
    for word in freq.keys():
        prob[word] = freq[word]*1.0/total_count

    return prob

# Get Probability of given label


def get_tweet_label_count(training_data, label):
    count = 0
    total_count = 0
    for data in training_data:
        total_count += 1
        if data[0] == label:
            count += 1
    return count*1.0/total_count

# Label the test data given the trained parameters Using Naive Bayes Model


def label_data(quantity, obj, test_data, sports_word_prob, politics_word_prob, tech_word_prob, sports_prob, politics_prob, tech_prob):
    labels = []
    politics = 0 
    sports = 0 
    technology = 0 
    for i, data in enumerate(test_data):
        data_prob_sports = sports_prob
        data_prob_politics = politics_prob
        data_prob_tech = tech_prob

        for word in data[1]:
            if word in sports_word_prob:
                data_prob_sports *= sports_word_prob[word]
                data_prob_politics *= politics_word_prob[word]
                data_prob_tech *= tech_word_prob[word]
            else:
                continue

        if (data_prob_sports >= data_prob_politics) and (data_prob_sports >= data_prob_tech):
            obj.get('tweets')[i].append('Sports')
            sports += 1
        elif (data_prob_politics >= data_prob_sports) and (data_prob_politics >= data_prob_tech):
            obj.get('tweets')[i].append('Politics')
            politics += 1
        else:
            obj.get('tweets')[i].append('Technology')
            technology += 1
    
    obj['sports'] = round(sports/quantity *100)
    obj['politics'] = round(politics/quantity *100)
    obj['technology'] = round(technology/quantity *100)
    obj['user']= True
    return obj

# Print the labelled test data


def print_labelled_data(labels):
    f_out = open('C:\\Users\\arham\\OneDrive\\Desktop\\Output.txt',
                 'w', encoding='utf-8')
    for [label, tweet, prob_sports, prob_politics] in labels:
        f_out.write('%s %s\n' % (label, tweet))

    f_out.close()


def callNaiveBayes(username, quantity):

    # Get the training and test data
    temp = test_data = get_tweet_test_data(username, quantity)
    if(temp == 0):
        return {'user':False}

    test_data, obj = temp
    training_data = get_tweet_training_data()

    # Get the probabilities of each word overall and in the two labels
    word_prob = get_tweet_word_prob(training_data)
    sports_word_prob = get_tweet_word_prob(training_data, 'Sports')
    politics_word_prob = get_tweet_word_prob(training_data, 'Politics')
    tech_word_prob = get_tweet_word_prob(training_data, 'Technology')

    # Get the probability of each label
    sports_prob = get_tweet_label_count(training_data, 'Sports')
    politics_prob = get_tweet_label_count(training_data, 'Politics')
    tech_prob = get_tweet_label_count(training_data, 'Technology')

    # Normalise for stop words
    for (word, prob) in word_prob.items():
        sports_word_prob[word] /= prob
        politics_word_prob[word] /= prob
        tech_word_prob[word] /= prob

    # Label the test data and print it
    return  label_data(quantity, obj, test_data, sports_word_prob, politics_word_prob,
                             tech_word_prob, sports_prob, politics_prob, tech_prob)
