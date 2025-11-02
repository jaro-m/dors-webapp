import axios from "axios";

const baseURL = process.env.REACT_APP_API_URL

console.log(`REACT_APP_API_URL: ${ baseURL }`);

export const Api = axios.create({
  baseURL: `${baseURL}/api`,
});


export const getToken = async (requestBody) => {
  try {
    const response = await Api.post(`${baseURL}/token`, requestBody);
    return response;
  } catch(err) {
    throw err
  }
}


const sendRequest = async (method, endpoint, data = {}) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  try {
    let result = {};
    if (method.toLowerCase() === "get") {
      result =  await Api.get(endpoint, config);
    } else if (method.toLowerCase() === "post") {
      result = await Api.post(endpoint, data, config);;
    } else if (method.toLowerCase() === "put") {
      result = await Api.put(endpoint, data, config)
    } else {
      console.log(`incorrect method: ${method}`);
      return { error: `incorrect method: ${method}`};
    }
    return result;
  } catch(err) {
    console.log({ err }, "API Error");
    if (err?.status && (err.status === 401 || err.status === 403)) {
      sessionStorage.removeItem('access_token')
      return { error: "not authorized"};
    }
    console.log({ err });
    return({error: err});
  }
};

export const getReports = async () => {
  const result = await sendRequest('GET', '/reports');
  return result;
};

export const getReport = async (id) => {
  const result = await sendRequest('GET', `/reports/${id}`);
  return result;
};

export const getReporter = async (id) => {
  const result = await sendRequest('GET', `/reports/${id}/reporter`);
  return result;
};

export const getPatient = async (id) => {
  const result = await sendRequest('GET', `/reports/${id}/patient`);
  return result;
};

export const getDisease = async (id) => {
  const result = await sendRequest('GET', `/reports/${id}/disease`);
  return result;
};

export const getRecent = async () => {
  const result = await sendRequest('GET', '/reports/recent');
  return result;
};

export const postReporter = async (reporter) => {
  const result = await sendRequest('post', `/reports/${reporter.id}/reporter`, reporter);
  return result;
};

export const postPatient = async (patient) => {
  const result = await sendRequest('post', `/reports/${patient.id}/patient`, patient);
  return result;
};

export const postDisease = async (disease) => {
    const result = await sendRequest('post', `/reports/${disease.id}/disease`, disease);
    return result;
};

export const putReport = async (report) => {
  const result = await Api.put(`/reports/${report.id}`, report);
  return result;
};

