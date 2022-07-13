from logzero import logger


def suggestion_json_fixer(json_file, source_id):
    fixed_json = list()
    if source_id == 1:
        for item in json_file:
            if 'Product Type/Family' not in item:
                continue
            if item['Product Type/Family'] == 'RAM':
                try:
                    integrated_memory_suggestion = dict(Title=item.get('title', "no info"),
                                                        Capacity=item.get('Memory Capacity', "no info"),
                                                        Speed=item.get('Speed (Data Rate)', "no info"),
                                                        ManufactureTech=item.get('Form Factor', "no info"),
                                                        ModuleType=item.get('Module Type', "no info"),
                                                        Voltage=item.get('Memory Voltage', "no info"),
                                                        Specs=[item.get('CAS Latency', "no info"),
                                                               item.get('Memory Voltage', "no info"),
                                                               item.get('Module Type', "no info"),
                                                               item.get('Error Check', "no info"),
                                                               item.get('Pins', "no info"),
                                                               item.get('Rank', "no info"),
                                                               item.get('Chip Organization', "no info"),
                                                               item.get('Form Factor', "no info"),
                                                               item.get('Speed (Data Rate)', "no info")],
                                                        Category=item.get('Product Type/Family', "no info"))
                except Exception as e:
                    logger.exception(e)
                    integrated_memory_suggestion = dict(Title=item['title'], Status='This item has Error')
                fixed_json.append(integrated_memory_suggestion)
            elif item['Product Type/Family'] == 'SSD':
                try:
                    if 'Portable Drive Capacity' in item:
                        integrated_portal_suggestion = dict(Title=item['title'],
                                                            Capacity=item['Portable Drive Capacity'],
                                                            Specs=[f"Read Speed: {item['Read Speed']}",
                                                                   f"Write Speed: {item['Write Speed'] if 'Write Speed' in item else 'N/A'}"],
                                                            Category='ExternalSSD')
                        fixed_json.append(integrated_portal_suggestion)
                    else:
                        integrated_storage_suggestion = dict(Title=item['title'], Capacity=item['SSD Capacity'],
                                                             Interface=item['SSD Host Interface'],
                                                             FormFactor=item['SSD Form Factor'],
                                                             Specs=[item['SSD Capacity'], item['SSD Host Interface'],
                                                                    item['Read Speed'], item['Write Speed']],
                                                             Category=item['Product Type/Family'])
                        fixed_json.append(integrated_storage_suggestion)
                except Exception as e:
                    logger.exception(e)
                    integrated_storage_suggestion = dict(Title=item['title'], Status='This item has Error',
                                                         Category=item['Product Type/Family'])
                    fixed_json.append(integrated_storage_suggestion)
    elif source_id == 2:
        for item in json_file['memory']:
            try:
                integrated_memory_suggestion = dict(Title=item['title'], Capacity=item['total-capacity'],
                                                    Speed=item['speed'], ManufactureTech=item['technology'],
                                                    ModuleType=item['module-type'], Voltage=item['voltage'],
                                                    Specs=item['specs'], Category='memory')
            except Exception as e:
                logger.exception(e)
                integrated_memory_suggestion = dict(Title=item['title'], Status='This item has Error')
            fixed_json.append(integrated_memory_suggestion)
        for item in json_file['ssd']:
            try:
                integrated_storage_suggestion = dict(Title=item['title'],
                                                     Capacity=item['density-ssd'] if 'density-ssd' in item else item[
                                                         'density-range'],
                                                     Interface=item['interface'], FormFactor=item['form-factor'],
                                                     Specs=item['specs'], Category='ssd')
            except Exception as e:
                logger.exception(e)
                integrated_storage_suggestion = dict(Title=item['title'], Status='This item has Error')
            fixed_json.append(integrated_storage_suggestion)
        for item in json_file['Externalssd']:
            integrated_portable_suggestion = dict(Title=item['title'],
                                                  Capacity=item['density-ssd'] if 'density-ssd' in item else item[
                                                      'density-range'],
                                                  Specs=item['specs'], Category='Externalssd')
            fixed_json.append(integrated_portable_suggestion)
    else:
        raise NotImplementedError
    return fixed_json
