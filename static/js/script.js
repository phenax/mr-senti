

const fetcher = (url, request) => {
	if(request.query) {
		request.queryString=
			Object
				.keys(request.query)
				.map(key => `${key}=${request.query[key]}`)
				.join('&');

		url+= '?' + request.queryString;
	}

	return fetch(url, request);
};

const $result= document.querySelector('.js-result-dump');


document
	.querySelector('.js-form-submit')
	.addEventListener('submit', e => {
		e.preventDefault();

		const data= new FormData(e.currentTarget);

		const options= {
			method: 'GET',
			query: {
				text: data.get('text')
			}
		};

		fetcher('/api/analyse', options)
			.then(resp => resp.json())
			.then(resp => {
				$result.textContent = resp.label === 'pos'? '😃': '😞';
				console.log(resp.probabilities)
			});

		return false;
	});
