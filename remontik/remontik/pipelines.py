import json

from itemadapter import ItemAdapter


class RemontikPipeline:
    def process_item(self, item, spider):
        return item


class RemontikPipelineJson:
    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False, indent=4, default=str) + ",\n"
        self.file.write(line)
        return item

    def open_spider(self, spider):
        self.file = open('result.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()