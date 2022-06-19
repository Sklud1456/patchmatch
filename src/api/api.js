import axios from 'axios';

let base = 'http://127.0.0.1:5000/api';

export const requestLogin = params => {
    return axios({
        method: 'POST',
        url: `${base}/login`,
        auth: params
    })
    .then(res => res.data);
};

export const setpwd = params => {
    return axios.post(`${base}/setpwd`, params);
};

export const getUserListPage = params => {
    return axios.get(`${base}/users/listpage`, { params: params });
};



export const getCommitListPage = params => {
    return axios.get(`${base}/CommitPage`, { params: params });
};

export const getCVEListPage = params => {
    return axios.get(`${base}/CVEPage`, { params: params });
};

export const getCVEPieChart = () => {
    return axios.get(`${base}/GetCVEPieChart`);
};

export const getCVELineChart = () => {
    return axios.get(`${base}/GetCVEYearLineChart`);
};

export const getCVEWatchChart = () => {
    return axios.get(`${base}/GetCVEWatchChart`);
};

export const getCVECircleChart = () => {
    return axios.get(`${base}/GetCVECircleChart`);
};

export const getCVESquareChart = () => {
    return axios.get(`${base}/GetCVESquareChart`);
};

export const getNewCVEs = () => {
    return axios.get(`${base}/GetNewCVETable`);
};

export const getSignalCVE = params => {
    return axios.get(`${base}/GetSingalCVE`,{ params: params });
};

export const getPredictRank = params => {
    return axios.get(`${base}/Predict`,{ params: params });
};

export const CheckCommit = params => {
    return axios.get(`${base}/CheckCommit`,{ params: params });
};

export const getNewCommits = () => {
    return axios.get(`${base}/GetNewCommitTable`);
};

export const getCommitPieChart = () => {
    return axios.get(`${base}/GetCommitPieChart`);
};

export const addNewCVE = params => {
    return axios.get(`${base}/AddNewCVE`,{ params: params });
};

export const addNewCommit = params => {
    return axios.get(`${base}/AddNewCommit`,{ params: params });
};





export const removeUser = params => {
    return axios.get(`${base}/user/remove`, { params: params });
};

export const batchRemoveUser = params => {
    return axios.get(`${base}/user/bathremove`, { params: params });
};

export const getdrawPieChart = () => {
    return axios.get(`${base}/getdrawPieChart`);
};

export const getdrawLineChart = () => {
    return axios.get(`${base}/getdrawLineChart`);
};