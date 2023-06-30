from __future__ import annotations

import csv
import re

from parsel import Selector
from playwright.async_api import async_playwright


class DataCollector:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    async def initialize(self):
        self.playwright, self.browser, self.page = await self.setup_browser()

    async def setup_browser(self):
        playwright = await async_playwright().start()

        browser = await playwright.chromium.launch(
            # headless=False,
            channel='chrome',
            args=['--disable-blink-features', '--disable-blink-features=AutomationControlled'],
            # timeout=0
        )

        context = await browser.new_context(
            user_agent=(
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                '(KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            ),

        )

        page = await context.new_page()
        page.set_default_timeout(0)
        return playwright, browser, page

    def build_url(self):
        BASE_URL = 'https://reservation.pc.gc.ca/create-booking/results?'
        map_id = f'mapId={-2147483183}'
        search_tab_group_id = f'searchTabGroupId={0}'
        booking_category_id = f'bookingCategoryId={0}'
        start_date = f'startDate={self.start_date}'
        end_date = f'endDate={self.end_date}'
        nights = 'nights=1'
        is_reserving = 'isReserving=true'
        equipment_id = f'equipmentId={-32768}'
        sub_equipment_id = f'subEquipmentId={-32767}'
        party_size = 'partySize=1'
        equipment_capacity = 'equipmentCapacity=1'
        filter_data = 'filterData=%7B%22-32756%22:%22%5B%5B1%5D,0,0,0%5D%22%7D'
        search_time = 'searchTime=2023-06-29T09:16:14.289'
        resource_location_id = f'resourceLocationId={-2147483540}'

        filter_query = '&'.join([
            map_id, search_tab_group_id, booking_category_id, start_date, end_date, nights,
            is_reserving, equipment_id, sub_equipment_id, party_size, equipment_capacity, filter_data, search_time,
            resource_location_id,
        ])

        print('Filter Query:')
        print(filter_query)
        print()

        complete_url = f'{BASE_URL}{filter_query}'

        print('Complete URL:')
        print(complete_url)
        print()

        RAW_COPY_URL = (
            'https://reservation.pc.gc.ca/create-booking/results'
            '?mapId=-2147483183&searchTabGroupId=0&bookingCategoryId=0&startDate=2023-08-22'
            '&endDate=2023-08-23'
            '&nights=1&isReserving=true&equipmentId=-32768&subEquipmentId=-32767&partySize=1'
            '&equipmentCapacity=1&filterData=%7B%22-32756%22:%22%5B%5B1%5D,0,0,0%5D%22%7D'
            '&searchTime=2023-06-29T09:16:14.289&resourceLocationId=-2147483540'
        )
        print('Raw Copy URL:')
        print(RAW_COPY_URL)

        return complete_url

    async def fetch_html_content(self):
        url = self.build_url()
        await self.page.goto(url)

        # Selecting list and details button
        await self.page.locator('#list-view-button-button').click()
        await self.page.locator("//div[@class='btn-view-details ng-star-inserted']").click()
        await self.page.wait_for_timeout(1500)

        html = await self.page.content()
        response = Selector(text=html)

        await self.browser.close()
        await self.playwright.stop()

        return response

    def clean_data(self, data):
        pattern = r':\s(.*)'
        return re.search(pattern, data).group(1) if data else None

    async def extract_data(self):
        response = await self.fetch_html_content()

        # Xpath code
        name = response.xpath("//div[@class='side-bar-content']//h2/text()").get()
        nightly_fees = response.xpath(
            "//div[@class='site-details-wrapper ng-star-inserted']//div[@class='bold']/text()",
        ).get()

        max_capacity = self.clean_data(response.xpath("//span[starts-with(text(), 'Max Capacity')]/text()").get())
        sub_category = self.clean_data(response.xpath("//span[starts-with(text(), 'Sub-Category')]/text()").get())
        service_level = self.clean_data(response.xpath("//span[starts-with(text(), 'Service Level')]/text()").get())
        service_type = self.clean_data(response.xpath("//span[starts-with(text(), 'Service Type')]/text()").get())
        electrical_service = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Electrical Service')]/text()",
            ).get(),
        )
        water_service = self.clean_data(response.xpath("//span[starts-with(text(), 'Water Service')]/text()").get())
        sewer_service = self.clean_data(response.xpath("//span[starts-with(text(), 'Sewer Service')]/text()").get())
        accessible = self.clean_data(response.xpath("//span[starts-with(text(), 'Accessible')]/text()").get())
        pull_through = self.clean_data(response.xpath("//span[starts-with(text(), 'Pull-through')]/text()").get())
        maneuverability = self.clean_data(response.xpath("//span[starts-with(text(), 'Maneuverability')]/text()").get())
        site_size = self.clean_data(response.xpath("//span[starts-with(text(), 'Site Size')]/text()").get())
        ground_cover = self.clean_data(response.xpath("//span[starts-with(text(), 'Ground Cover')]/text()").get())
        campsite_slope = self.clean_data(response.xpath("//span[starts-with(text(), 'Campsite Slope')]/text()").get())
        main_pad_cover = self.clean_data(response.xpath("//span[starts-with(text(), 'Main Pad Cover')]/text()").get())
        main_pad_slope = self.clean_data(response.xpath("//span[starts-with(text(), 'Main Pad Slope')]/text()").get())
        additional_pad_cover = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Additional Pad Cover')]/text()",
            ).get(),
        )
        swimming_conditions = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Swimming Conditions')]/text()",
            ).get(),
        )
        waterfront = self.clean_data(response.xpath("//span[starts-with(text(), 'Waterfront')]/text()").get())
        walk_in_only = self.clean_data(response.xpath("//span[starts-with(text(), 'Walk-in Only')]/text()").get())
        firepit_on_site = self.clean_data(response.xpath("//span[starts-with(text(), 'Firepit On Site')]/text()").get())
        picnic_table = self.clean_data(response.xpath("//span[starts-with(text(), 'Picnic Table')]/text()").get())
        off_site_vehicle_parking = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Off-Site Vehicle Parking')]/text()",
            ).get(),
        )
        cellular_coverage = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Cellular Coverage')]/text()",
            ).get(),
        )
        wifi = self.clean_data(response.xpath("//span[starts-with(text(), 'Wi-fi')]/text()").get())
        distance_to_washroom_facilities = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Distance to Washroom Facilities')]/text()",
            ).get(),
        )
        distance_to_shower_facilities = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Distance to Shower Facilities')]/text()",
            ).get(),
        )
        distance_to_cooking_shelter = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Distance to Cooking/Kitchen Shelter')]/text()",
            ).get(),
        )
        distance_to_water_tap = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Distance to Water Tap')]/text()",
            ).get(),
        )
        site_shade = self.clean_data(response.xpath("//span[starts-with(text(), 'Site Shade')]/text()").get())
        privacy = self.clean_data(response.xpath("//span[starts-with(text(), 'Privacy')]/text()").get())
        generator_usage = self.clean_data(response.xpath("//span[starts-with(text(), 'Generator Usage')]/text()").get())
        distance_to_playground = self.clean_data(
            response.xpath(
                "//span[starts-with(text(), 'Distance to Playground')]/text()",
            ).get(),
        )
        adjacent_to = self.clean_data(response.xpath("//span[starts-with(text(), 'Adjacent To')]/text()").get())
        main_pad_width = self.clean_data(response.xpath("//span[starts-with(text(), 'Main Pad Width')]/text()").get())
        main_pad_length = self.clean_data(response.xpath("//span[starts-with(text(), 'Main Pad Length')]/text()").get())
        site_length = self.clean_data(response.xpath("//span[starts-with(text(), 'Site Length')]/text()").get())
        firepit_type = self.clean_data(response.xpath("//span[starts-with(text(), 'Firepit Type')]/text()").get())

        # Data will store here
        data = []

        data.append({
            'name': name,
            'nightly_fees': nightly_fees,
            'max_capacity': max_capacity,
            'sub_category': sub_category,
            'service_level': service_level,
            'service_type': service_type,
            'electrical_service': electrical_service,
            'water_service': water_service,
            'sewer_service': sewer_service,
            'accessible': accessible,
            'pull_through': pull_through,
            'maneuverability': maneuverability,
            'site_size': site_size,
            'ground_cover': ground_cover,
            'campsite_slope': campsite_slope,
            'main_pad_cover': main_pad_cover,
            'main_pad_slope': main_pad_slope,
            'additional_pad_cover': additional_pad_cover,
            'swimming_conditions': swimming_conditions,
            'waterfront': waterfront,
            'walk_in_only': walk_in_only,
            'firepit_on_site': firepit_on_site,
            'picnic_table': picnic_table,
            'off_site_vehicle_parking': off_site_vehicle_parking,
            'cellular_coverage': cellular_coverage,
            'wifi': wifi,
            'distance_to_washroom_facilities': distance_to_washroom_facilities,
            'distance_to_shower_facilities': distance_to_shower_facilities,
            'distance_to_cooking_shelter': distance_to_cooking_shelter,
            'distance_to_water_tap': distance_to_water_tap,
            'site_shade': site_shade,
            'privacy': privacy,
            'generator_usage': generator_usage,
            'distance_to_playground': distance_to_playground,
            'adjacent_to': adjacent_to,
            'main_pad_width': main_pad_width,
            'main_pad_length': main_pad_length,
            'site_length': site_length,
            'firepit_type': firepit_type,
        })

        return data

    async def extract_to_csv(self):
        data = self.extract_data()

        csv_file_name = 'data.csv'
        fieldnames = [
            'name',
            'nightly_fees',
            'max_capacity',
            'sub_category',
            'service_level',
            'service_type',
            'electrical_service',
            'water_service',
            'sewer_service',
            'accessible',
            'pull_through',
            'maneuverability',
            'site_size',
            'ground_cover',
            'campsite_slope',
            'main_pad_cover',
            'main_pad_slope',
            'additional_pad_cover',
            'swimming_conditions',
            'waterfront',
            'walk_in_only',
            'firepit_on_site',
            'picnic_table',
            'off_site_vehicle_parking',
            'cellular_coverage',
            'wifi',
            'distance_to_washroom_facilities',
            'distance_to_shower_facilities',
            'distance_to_cooking_shelter',
            'distance_to_water_tap',
            'site_shade',
            'privacy',
            'generator_usage',
            'distance_to_playground',
            'adjacent_to',
            'main_pad_width',
            'main_pad_length',
            'site_length',
            'firepit_type',
        ]
        with open(csv_file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print('CSV file saved successfully!')
