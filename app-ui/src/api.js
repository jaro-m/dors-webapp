import axios from "axios";

export const Api = axios.create({
  baseURL: "https://localhost:8000/api",
});


export const getReports = async () => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  try {
    const result = await Api.get(`/reports`, config);
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

export const getReport = async (id) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  try {
    const result = await Api.get(`/reports/${id}`, config);
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

export const getRecent = async (id) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  try {
    const result = await Api.get(`/reports/recent`, config);
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

export const getReporter = async (id) => {
  console.log(`getReporter API func(), ID =====>>>>> ${id}`);
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  try {
    const result = await Api.get(`/reports/${id}/reporter`, config);
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

export const getPatient = async (id) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  try {
    const result = await Api.get(`/reports/${id}/patient`, config);
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

export const getDisease = async (id) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  try {
    const result = await Api.get(`/reports/${id}/disease`, config);
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

export const postReporter = async (reporter) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  console.log({ reporter }, "POST reporter data");
  try {
    const result = await Api.post(`/reports/${reporter.id}/reporter`, reporter, config);
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

export const postPatient = async (patient) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  console.log({ patient }, "POST patient data");
  try {
    const result = await Api.post(`/reports/${patient.id}/patient`, patient, config);
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

export const postDisease = async (disease) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  console.log({ disease }, "POST disease data");
  try {
    const result = await Api.post(`/reports/${disease.id}/disease`, disease, config);
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

export const putReport = async (report) => {
  const config = {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('access_token')}`,
    }
  }
  console.log({ report }, "PUT report data");
  try {
    const result = await Api.put(`/reports/${report.id}`, report, config);
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

