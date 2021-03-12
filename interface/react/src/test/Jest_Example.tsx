
export const add = (x, y) => { return x + y; };

export const newTotal = (price, oldTotal) => {return '$' + add(price, oldTotal)};

export const functionNotExported = (x, y) => {return true};