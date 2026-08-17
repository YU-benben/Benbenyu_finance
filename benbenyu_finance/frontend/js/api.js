/**
 * 笨笨鱼财务系统 - 前端 API 封装
 * 统一管理后端接口请求与 Token
 */

const API_BASE = 'http://127.0.0.1:8000';

/** 获取本地存储的 Token */
function getToken() {
  return localStorage.getItem('token');
}

/** 保存登录信息到本地 */
function saveAuth(data) {
  localStorage.setItem('token', data.access_token);
  localStorage.setItem('role', data.role);
  localStorage.setItem('display_name', data.display_name);
  if (data.org_name) {
    localStorage.setItem('org_name', data.org_name);
  }
}

/** 清除登录信息 */
function clearAuth() {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  localStorage.removeItem('display_name');
  localStorage.removeItem('org_name');
}

/** 检查是否已登录，未登录则跳转 */
function requireAuth(expectedRole) {
  const token = getToken();
  const role = localStorage.getItem('role');
  if (!token) {
    window.location.href = 'index.html';
    return false;
  }
  if (expectedRole && role !== expectedRole) {
    window.location.href = role === 'organization' ? 'org.html' : 'personal.html';
    return false;
  }
  return true;
}

/** 通用请求方法 */
async function request(url, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  const token = getToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    clearAuth();
    window.location.href = 'index.html';
    throw new Error('登录已过期，请重新登录');
  }

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    const detail = err.detail;
    const msg = Array.isArray(detail) ? detail.map(d => d.msg || d).join('; ') : (detail || '请求失败');
    throw new Error(msg);
  }

  // 处理文件下载
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('spreadsheetml') || contentType.includes('octet-stream')) {
    return response;
  }

  return response.json();
}

/** API 接口集合 */
const api = {
  /** 登录 */
  login(username, password, role) {
    return request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password, role }),
    });
  },

  /** 个人用户 - 查询记录 */
  getPersonalRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return request(`/api/personal/records?${qs}`);
  },

  /** 个人用户 - 新增记录 */
  createPersonalRecord(data) {
    return request('/api/personal/records', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /** 个人用户 - 更新记录 */
  updatePersonalRecord(id, data) {
    return request(`/api/personal/records/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /** 个人用户 - 删除记录 */
  deletePersonalRecord(id) {
    return request(`/api/personal/records/${id}`, { method: 'DELETE' });
  },

  /** 个人用户 - 统计 */
  getPersonalStatistics(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return request(`/api/personal/statistics?${qs}`);
  },

  /** 个人用户 - 导出 Excel */
  async exportPersonal(params = {}) {
    const qs = new URLSearchParams(params).toString();
    const response = await request(`/api/personal/export?${qs}`);
    return response.blob();
  },

  /** 单位用户 - 查询记录 */
  getOrgRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return request(`/api/org/records?${qs}`);
  },

  /** 单位用户 - 新增记录 */
  createOrgRecord(data) {
    return request('/api/org/records', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /** 单位用户 - 更新记录 */
  updateOrgRecord(id, data) {
    return request(`/api/org/records/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /** 单位用户 - 删除记录 */
  deleteOrgRecord(id) {
    return request(`/api/org/records/${id}`, { method: 'DELETE' });
  },

  /** 单位用户 - 统计 */
  getOrgStatistics(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return request(`/api/org/statistics?${qs}`);
  },

  /** 单位用户 - 导出 Excel */
  async exportOrg(params = {}) {
    const qs = new URLSearchParams(params).toString();
    const response = await request(`/api/org/export?${qs}`);
    return response.blob();
  },
};

/** 下载 Blob 文件 */
function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

/** 格式化金额 */
function formatMoney(value) {
  return Number(value || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

/** 获取今天日期字符串 YYYY-MM-DD */
function todayStr() {
  return new Date().toISOString().slice(0, 10);
}
