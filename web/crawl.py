import save
import down
import extract

def launch(inst):
	while True:
		urls, hashes = down.get_urls(inst)
		for i in range(len(urls)):
			url, hash = urls[i], hashes[i]
			content = down.get_content(url)
			print(inst, url)
			if content is not None:
				links, words = extract.extract(content, url)
				print(len(links), len(words))
				url_id = save.get_id(hash)
				save.save_urls(links, url_id)
				save.save_words(words.keys(), words.values(), url_id)