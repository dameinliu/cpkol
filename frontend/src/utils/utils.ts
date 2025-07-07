/**
 * 时间格式化：支持时间戳（秒）或 ISO 字符串，返回本地日期（只到天）
 */
export function formatTime(input?: number | string): string {
  if (!input) return '-'
  let d: Date
  if (typeof input === 'number') {
    d = new Date(input * 1000)
  } else if (typeof input === 'string') {
    d = new Date(input)
  } else {
    return '-'
  }
  return d.toLocaleDateString()
}

/** 计算百分比，保留两位小数 */
export function percent(a: number, b: number): string {
  if (!b || b === 0) return '0%'
  return ((a / b) * 100).toFixed(2) + '%'
}

/** 计算平均值，保留两位小数 */
export function avg(total: number, count: number): string {
  if (!count || count === 0) return '0'
  return (total / count).toFixed(2)
}