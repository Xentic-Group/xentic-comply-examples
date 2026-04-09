const axios = require('axios');

// Get your rapidapi key from https://rapidapi.com/xentic-xentic-default/api/xentic-comply-api
const RAPIDAPI_KEY = process.env.RAPIDAPI_KEY || 'YOUR_RAPIDAPI_KEY_HERE';

async function scanWebsite(domain, countryCode = 'EU') {
  console.log(`Analyzing ${domain} for ${countryCode} compliance...`);

  const options = {
    method: 'POST',
    url: 'https://xentic-comply-api.p.rapidapi.com/v1/scan',
    headers: {
      'content-type': 'application/json',
      'x-rapidapi-host': 'xentic-comply-api.p.rapidapi.com',
      'x-rapidapi-key': RAPIDAPI_KEY
    },
    data: {
      domain: domain,
      country_code: countryCode,
      include_pdf: false // Available on PRO+ plans
    }
  };

  try {
    const response = await axios.request(options);
    const data = response.data;
    
    console.log('\n✅ SCAN SUCCESSFUL');
    console.log(`Overall Score: ${data.score}/100`);
    console.log(`Letter Grade:  ${data.grade}`);
    console.log(`Scan ID:       ${data.scan_id}`);
    
    console.log('\nDetailed Breakdown:');
    data.checks.forEach(check => {
      const statusIcon = check.passed ? '✅' : '❌';
      console.log(`${statusIcon} ${check.name} (${check.severity})`);
      if (!check.passed) {
        console.log(`   Detail: ${check.detail}`);
        console.log(`   Fix:    ${check.recommendation}`);
      }
    });

  } catch (error) {
    console.error('❌ SCAN FAILED');
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error(`Status: ${error.response.status}`);
      console.error(error.response.data);
    } else {
      console.error(error.message);
    }
  }
}

// Ensure you run this script with your API key set, e.g.:
// export RAPIDAPI_KEY="your-key-here" && node scan_with_axios.js
scanWebsite('xentic.cloud', 'PA');
