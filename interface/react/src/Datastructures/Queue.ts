import React from 'react'

export default class Queue {
    count;
    lowestCount;
    items;

    constructor() {
        this.count = 0;
        this.lowestCount = 0;
        this.items = {};
    }

    enqueue(element){
        this.items[this.count] = element;
        this.count ++;
    }


    dequeue(){
        if (this.isEmpty()) {
            return undefined;
        }
        let result = this.items[this.lowestCount];
        delete this.items[this.lowestCount];
        this.lowestCount++;
        return result;

    }

    front(){
        if (this.isEmpty()) {
            return undefined;
        }
        return this.items[this.lowestCount];

    }


    size() {
        return this.count - this.lowestCount;
    }


    isEmpty() {
        return this.size() === 0;
    }

    clear() {
        this.items = {}
        this.count = 0;
        this.lowestCount = 0;
        return this.items;
    }

}

