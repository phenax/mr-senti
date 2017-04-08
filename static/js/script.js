
// Where to dump the resulting emoji/score
const $result= document.querySelector('.js-result-dump');



/**
 * Fetch with query object
 */
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

/**
 * Get fetch options
 * 
 * @param  {FormData|Map} data
 * 
 * @return {Object}
 */
const getOptions = data => ({
	method: 'GET',
	query: {
		text: data.get('text')
	}
});


// Log stuff and return stuff
const logger = stuff => { console.log(stuff); return stuff; };


/**
 * Analyse the text and return a promise for an emoji
 * 
 * @param  {FormData} data
 * 
 * @return {Promise}
 */
const analyseSentiment = data =>
	fetcher('/api/analyse', getOptions(data))
		.then(resp => resp.json())
		.then(logger)
		.then(resp => resp.label === 'pos'? 'smile': 'frown');


/**
 * Render icon
 * 
 * @param  {string} icon
 */
const renderIcon = icon =>
	$result.innerHTML = `<i class="fa fa-${icon}-o"></i>`;



document
	.querySelector('.js-form-submit')
	.addEventListener('submit', e => {
		e.preventDefault();

		const data= new FormData(e.currentTarget);

		// Analyse sentiment and then render the icon
		analyseSentiment(data).then(renderIcon);

		return false;
	});
